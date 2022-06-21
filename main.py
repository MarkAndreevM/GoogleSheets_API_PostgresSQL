from __future__ import print_function

import re
import time
from datetime import datetime

from googleapiclient.discovery import build
from google.oauth2 import service_account

from data_base import sql_start, sql_update, sql_delete_task, sql_get_select_all_data
from functional import conversion_dollar_to_ruble


# Подключаемся к учётной записи Google API
SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Создаем экземпляр учетных данных из файла json
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# ID таблицы
SAMPLE_SPREADSHEET_ID = '1zWDJZ_SQG89EazUb-jrRALxq8orM58RZmVrr1TZq_PE'
# получаем доступ к таблице
service = build('sheets', 'v4', credentials=creds)


convert_dollar_in_rub = conversion_dollar_to_ruble()


def rework_res(res: list, length=4):
    """
    Заполняет вложенные списки пустыми строками до нужной длины списка.
    """
    for i in res:
        i += [''] * (length - len(i))
        i[0] = i[0] if i[0].isdigit() else 'DEFAULT'
        i[1] = i[1] if i[1].isdigit() else 'DEFAULT'
        i[2] = float(i[2]) * round(convert_dollar_in_rub, 2) if i[2].isdigit() else 0
        i[3] = i[3] if re.fullmatch(r'\d{2}[\.-]\d{2}[\.-]\d{4}', i[3]) else '01.01.1970'

#
# def convert_sheet_in_dict(sheets):
#     rework_res(sheets)
#


# получаем значения из таблицы
def get_sheets_data(service, sheet_id):
    # Вызываем таблицу (API)
    sheet = service.spreadsheets()
    values = sheet.values().get(spreadsheetId=sheet_id, range="A:D").execute()
    res = values.get('values', [])
    rework_res(res)
    dict_google_sheet = {i[1]: (i[0], i[2], i[3]) for i in res[1:]}  # Создаем словарь, где ключ - это номер заказа
    return dict_google_sheet


sql_start()  # Подключаемся к БД, создаем таблицу если "такой-то" таблицы нет
sql_data_cache = sql_get_select_all_data()
sql_data_cache = {str(i[1]): (i[0], round(i[2], 2), str(i[3])) for i in sql_data_cache}  # превращаем кэшируемые данные из SQL в словарь с ключом

while True:

    dict_google_sheet = get_sheets_data(service=service, sheet_id=SAMPLE_SPREADSHEET_ID)  # Пересобираем словарь (каждые 2 сек. >)

    #  Удаляем строку из БД если такого номера заказа в запросе d не нашлось
    for i in sql_data_cache:
        if i not in dict_google_sheet and i != 'DEFAULT':
            sql_delete_task(i)

    # Добавляем строку в БД если добавили новый номер заказа в GoogleSheets
    for i in dict_google_sheet:
        if i not in sql_data_cache and i != 'DEFAULT':
            try:
                datetime.strptime(dict_google_sheet[i][2], "%d-%m-%Y")  # Проверка правильности ввода даты
                sql_update(dict_google_sheet[i][0], i, dict_google_sheet[i][1], dict_google_sheet[i][2])  # Записывает новую строчку в БД
            except ValueError:
                sql_update(dict_google_sheet[i][0], i, dict_google_sheet[i][1], '01.01.1970')

    # Перезаписываем данные из словаря (если в БД данных не было у данного номера заказа (не успели заполнить) за цикл While True)
    for i in dict_google_sheet:
        if i in sql_data_cache and dict_google_sheet[i] != sql_data_cache[i]:
            if dict_google_sheet[i] != "DEFAULT":
                sql_delete_task(i)  # Удаляем ранее записанную строку с этим номером

            try:
                datetime.strptime(dict_google_sheet[i][2], "%d-%m-%Y")  # Проверка правильности ввода даты
                sql_update(dict_google_sheet[i][0], i, dict_google_sheet[i][1], dict_google_sheet[i][2])  # Обновляем строку с номером заказ со всеми данными из словаря
            except ValueError:
                sql_update(dict_google_sheet[i][0], i, dict_google_sheet[i][1], '01.01.1970')
    sql_data_cache = dict_google_sheet

    time.sleep(2)




    # if data_cache != d:  # перезаписываем данные в БД, если кэш из таблицы не равен обновлённым данным в таблице
    #     sql_delete_task()
    #     for i in tuple(result[1:]):
    #         sql_update(i[0], i[1], i[2], i[3])
    #
    #     data_cache = result














# sql_start()
# data_cache = {}
# # d = {i[1]:(i[0],i[2],i[3]) for i in result[1:]}  # Создаем словарь, где ключ - это номер заказа
# while True:
#     result = get_sheets_data(service=service, sheet_id=SAMPLE_SPREADSHEET_ID)
#     d = {i[1]: (i[0], i[2], i[3]) for i in result[1:]}  # Создаем словарь, где ключ - это номер заказа
#     rework_res(result)
#
#     if data_cache != result:  # перезаписываем данные в БД, если кэш из таблицы не равен обновлённым данным в таблице
#         sql_delete_task()
#         for i in tuple(result[1:]):
#             sql_update(i[0], i[1], i[2], i[3])
#
#         data_cache = result
#     time.sleep(2)

