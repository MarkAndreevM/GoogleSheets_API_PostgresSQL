from pycbrf.toolbox import ExchangeRates
import datetime

#  Функция отправляет запрос на сервис ЦБ РФ и возвращает курс рубля к доллару (в руб)
from data_base import sql_delete_task, sql_update

from googleapiclient.discovery import build
from google.oauth2 import service_account


def get_the_GoogleSheet_table_by_API():
    # Подключаемся к учётной записи Google API
    SERVICE_ACCOUNT_FILE = 'keys.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # Создаем экземпляр учетных данных из файла json
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # получаем доступ к таблице
    service = build('sheets', 'v4', credentials=creds)
    return service


def conversion_dollar_to_ruble():
    data = datetime.datetime.now()  # сегодняшнее число
    rates = ExchangeRates(data)  # Извлекаем обменные курсы
    res_convert = rates['USD'].value  # Нас интересуют $ доллары

    return float(res_convert)


#  Функция удаляет строку из БД если такого номера заказа в GoogleSheets не нашлось
def delete_line_in_SQL(sql_data_cache, dict_google_sheet):
    for i in sql_data_cache:
        if i not in dict_google_sheet and i != 'DEFAULT':
            sql_delete_task(i)


# Функция добавляет строку в БД если добавили новый номер заказа в GoogleSheets
def add_line_in_SQL(dict_google_sheet, sql_data_cache):
    for i in dict_google_sheet:
        if i not in sql_data_cache and i != 'DEFAULT':
            try:
                datetime.datetime.strptime(dict_google_sheet[i][2], "%d.%m.%Y")  # Проверка правильности ввода даты
                sql_update(dict_google_sheet[i][0], i, dict_google_sheet[i][1], dict_google_sheet[i][2])  # Записывает новую строчку в БД
            except ValueError:
                sql_update(dict_google_sheet[i][0], i, dict_google_sheet[i][1], '01.01.1970')


# Фнукция перезаписывает данные из словаря (если в БД данных не было у данного номера заказа (не успели заполнить) за цикл While True)
def rewrite_data_in_SQL(dict_google_sheet, sql_data_cache):
    for i in dict_google_sheet:
        if i in sql_data_cache and dict_google_sheet[i] != sql_data_cache[i] and dict_google_sheet[i] != "DEFAULT":
            sql_delete_task(i)  # Удаляем ранее записанную строку с этим номером
            try:
                datetime.datetime.strptime(dict_google_sheet[i][2], "%d.%m.%Y")  # Проверка правильности ввода даты
                sql_update(dict_google_sheet[i][0], i, dict_google_sheet[i][1], dict_google_sheet[i][2])  # Обновляем строку с номером заказ со всеми данными из словаря
            except ValueError:
                sql_update(dict_google_sheet[i][0], i, dict_google_sheet[i][1], '01.01.1970')


