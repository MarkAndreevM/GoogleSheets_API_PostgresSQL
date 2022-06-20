from __future__ import print_function
import re
import time

from config_project.config import SAMPLE_SPREADSHEET_ID
from data_base_PSQL.data_base import sql_start, sql_get_select_all_data
from func_logic.functional import conversion_dollar_to_ruble, delete_line_in_SQL, add_line_in_SQL, rewrite_data_in_SQL, \
    get_the_GoogleSheet_table_by_API


# получаем значения из таблицы
def get_sheets_data(service, sheet_id):
    """
    Функция возвращает данные из таблицы GoogleSheet, перезаписанные в словарь, где ключ это - номер заказа
    :param service: переменная в которой содержится путь к таблице GoogleSheets (получаем доступ к таблице)
    :param sheet_id: переменная SAMPLE_SPREADSHEET_ID - находится в модуле config (ID таблицы GoogleSheets)
    :return: cловарь, где ключ это - номер заказа
    """
    # Вызываем таблицу (API)
    sheet = service.spreadsheets()
    values = sheet.values().get(spreadsheetId=sheet_id, range="A:D").execute()
    res = values.get('values', [])
    rework_res(res)
    dict_google_sheet = {i[1]: (i[0], i[2], i[3]) for i in res[1:]}  # Создаем словарь, где ключ - это номер заказа
    return dict_google_sheet


def rework_res(res: list, length=4):
    """
    Заполняет вложенные списки пустыми строками до нужной длины списка (избегаем нежелательных ошибок).
    """
    for i in res:
        i += [''] * (length - len(i))
        i[0] = i[0] if i[0].isdigit() else 'DEFAULT'
        i[1] = i[1] if i[1].isdigit() else 'DEFAULT'
        i[2] = float(i[2]) * round(convert_dollar_in_rub, 2) if i[2].isdigit() else 0
        i[3] = i[3] if re.fullmatch(r'\d{2}[\.-]\d{2}[\.-]\d{4}', i[3]) else '01.01.1970'


if __name__ == "__main__":

    convert_dollar_in_rub = conversion_dollar_to_ruble()  # конвертируем доллары в рубли

    service = get_the_GoogleSheet_table_by_API()  # переменная, в которой содержится путь к GoogleSheets таблице

    sql_start()  # Подключаемся к БД, создаем таблицу если "такой-то" таблицы нет
    sql_data_cache = sql_get_select_all_data()
    sql_data_cache = {str(i[1]): (i[0], round(i[2], 2), str(i[3])) for i in sql_data_cache}  # превращаем кэшируемые данные из SQL в словарь с ключом

    while True:
        # Пересобираем словарь (каждые 2 сек.) Отслеживать обновление данных в GoogleSheets
        dict_google_sheet = get_sheets_data(service=service, sheet_id=SAMPLE_SPREADSHEET_ID)

        delete_line_in_SQL(sql_data_cache, dict_google_sheet)
        add_line_in_SQL(dict_google_sheet, sql_data_cache)
        rewrite_data_in_SQL(dict_google_sheet, sql_data_cache)

        sql_data_cache = dict_google_sheet  # Перезаписываем данные в кэше. Данные которые были добавлены в БД

        time.sleep(2)




