from pycbrf.toolbox import ExchangeRates  # Обменные курсы валют ЦБ РФ
from googleapiclient.discovery import build
from google.oauth2 import service_account


from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors

from data_base_PSQL.data_base import sql_delete_task, sql_add_line

import datetime


def get_the_GoogleSheet_table_by_API():
    """
    Возвращает значение переменной service
    в которой содержится путь к таблице GoogleSheets (получаем доступ к таблице)
    """
    # Подключаемся к учётной записи Google API
    SERVICE_ACCOUNT_FILE = './config_project/keys.json'  # путь к вашему json файлу
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # Создаем экземпляр учетных данных из файла json
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('sheets', 'v4', credentials=creds)
    return service


def conversion_dollar_to_ruble():
    """
    Отправляем запрос на сервис ЦБ РФ и возвращает курс рубля к доллару.
    """
    data = datetime.datetime.now()  # сегодняшнее число
    rates = ExchangeRates(data)  # Извлекаем обменные курсы
    res_convert = rates['USD'].value  # Нас интересуют доллары $

    return float(res_convert)


def delete_line_in_SQL(sql_data_cache, dict_google_sheet):
    """
    Удаляет строку из БД, если такого номера заказа в таблице GoogleSheets не нашлось.
    :param sql_data_cache: Кэш из БД
    :param dict_google_sheet: GoogleSheets таблица - перезаписанная в словарь, где ключ это - номер заказа
    """
    for i in sql_data_cache:
        if i not in dict_google_sheet and i != 'DEFAULT':
            sql_delete_task(i)  # Удаляем строку из БД (по номеру заказа), если в GoogleSheets нет такого номера


def add_line_in_SQL(dict_google_sheet, sql_data_cache):
    """
    Добавляем строку в БД, если добавили новый номер заказа в GoogleSheets
    :param dict_google_sheet: GoogleSheets таблица - перезаписанная в словарь, где ключ это - номер заказа.
    :param sql_data_cache: Кэш из БД
    """
    for i in dict_google_sheet:
        if i not in sql_data_cache and i != 'DEFAULT':
            try:
                datetime.datetime.strptime(dict_google_sheet[i][2], "%d.%m.%Y")  # Проверка правильности ввода даты
                sql_add_line(dict_google_sheet[i][0], i, dict_google_sheet[i][1], dict_google_sheet[i][2])  # Записывает новую строчку в БД
            except ValueError:
                sql_add_line(dict_google_sheet[i][0], i, dict_google_sheet[i][1], '01.01.1970')


def rewrite_data_in_SQL(dict_google_sheet, sql_data_cache):
    """
    Перезаписываем данные в БД (если в БД не хватало данных, у данного номера заказа (не успели заполнить)
    за цикл While True (за 2 сек))
    :param dict_google_sheet: GoogleSheets таблица - перезаписанная в словарь, где ключ это - номер заказа.
    :param sql_data_cache: Кэш из БД
    """
    for i in dict_google_sheet:
        if i in sql_data_cache and dict_google_sheet[i] != sql_data_cache[i] and dict_google_sheet[i] != "DEFAULT" and i != "DEFAULT":
            sql_delete_task(i)  # Удаляем ранее записанную строку с одним и тем же номером заказа.
            try:
                datetime.datetime.strptime(dict_google_sheet[i][2], "%d.%m.%Y")  # Проверка правильности ввода даты
                sql_add_line(sql_data_cache[i][0], i, dict_google_sheet[i][1], dict_google_sheet[i][2])  # Обновляем строку с номером заказ со всеми данными из словаря

            except ValueError:
                sql_add_line(dict_google_sheet[i][0], i, dict_google_sheet[i][1], '01.01.1970')

