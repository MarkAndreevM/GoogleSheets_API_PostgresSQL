from __future__ import print_function
import re
import time

from config import SAMPLE_SPREADSHEET_ID
from data_base import sql_start, sql_get_select_all_data
from functional_logic import conversion_dollar_to_ruble, delete_line_in_SQL, add_line_in_SQL, rewrite_data_in_SQL, \
    get_the_GoogleSheet_table_by_API


# получаем значения из таблицы
def get_sheets_data(service, sheet_id):
    # Вызываем таблицу (API)
    sheet = service.spreadsheets()
    values = sheet.values().get(spreadsheetId=sheet_id, range="A:D").execute()
    res = values.get('values', [])
    rework_res(res)
    dict_google_sheet = {i[1]: (i[0], i[2], i[3]) for i in res[1:]}  # Создаем словарь, где ключ - это номер заказа
    return dict_google_sheet


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


convert_dollar_in_rub = conversion_dollar_to_ruble()

if __name__ == "__main__":

    service = get_the_GoogleSheet_table_by_API()

    sql_start()  # Подключаемся к БД, создаем таблицу если "такой-то" таблицы нет
    sql_data_cache = sql_get_select_all_data()
    sql_data_cache = {str(i[1]): (i[0], round(i[2], 2), str(i[3])) for i in sql_data_cache}  # превращаем кэшируемые данные из SQL в словарь с ключом

    while True:

        dict_google_sheet = get_sheets_data(service=service, sheet_id=SAMPLE_SPREADSHEET_ID)  # Пересобираем словарь (каждые 2 сек. >)

        delete_line_in_SQL(sql_data_cache, dict_google_sheet)

        add_line_in_SQL(dict_google_sheet, sql_data_cache)

        rewrite_data_in_SQL(dict_google_sheet, sql_data_cache)

        sql_data_cache = dict_google_sheet

        time.sleep(2)
















#
#
# while True:
#
#     dict_google_sheet = get_sheets_data(service=service, sheet_id=SAMPLE_SPREADSHEET_ID)  # Пересобираем словарь (каждые 2 сек. >)
#
#     #  Удаляем строку из БД если такого номера заказа в запросе d не нашлось
#     for i in sql_data_cache:
#         if i not in dict_google_sheet and i != 'DEFAULT':
#             sql_delete_task(i)
#
#     # Добавляем строку в БД если добавили новый номер заказа в GoogleSheets
#     for i in dict_google_sheet:
#         if i not in sql_data_cache and i != 'DEFAULT':
#             try:
#                 datetime.strptime(dict_google_sheet[i][2], "%d-%m-%Y")  # Проверка правильности ввода даты
#                 sql_update(dict_google_sheet[i][0], i, dict_google_sheet[i][1], dict_google_sheet[i][2])  # Записывает новую строчку в БД
#             except ValueError:
#                 sql_update(dict_google_sheet[i][0], i, dict_google_sheet[i][1], '01.01.1970')
#
#     # Перезаписываем данные из словаря (если в БД данных не было у данного номера заказа (не успели заполнить) за цикл While True)
#     for i in dict_google_sheet:
#         if i in sql_data_cache and dict_google_sheet[i] != sql_data_cache[i]:
#             if dict_google_sheet[i] != "DEFAULT":
#                 sql_delete_task(i)  # Удаляем ранее записанную строку с этим номером
#
#             try:
#                 datetime.strptime(dict_google_sheet[i][2], "%d-%m-%Y")  # Проверка правильности ввода даты
#                 sql_update(dict_google_sheet[i][0], i, dict_google_sheet[i][1], dict_google_sheet[i][2])  # Обновляем строку с номером заказ со всеми данными из словаря
#             except ValueError:
#                 sql_update(dict_google_sheet[i][0], i, dict_google_sheet[i][1], '01.01.1970')
#     sql_data_cache = dict_google_sheet
#
#     time.sleep(2)

