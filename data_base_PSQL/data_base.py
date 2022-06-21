import psycopg2
from config_project.config import key_psycopg2_connect  # Импортируем подключение к PostgresSQL


def sql_execute(querry):
    """
    Избавляемся от DRY
    :param querry: запрос SQL (cur.execute)
    """
    conn = psycopg2.connect(key_psycopg2_connect)
    cur = conn.cursor()
    cur.execute(querry)
    conn.commit()
    conn.close()


def sql_start():
    """
    Подключаемся к PSQL, создаём таблицу
    """
    sql_execute("CREATE TABLE IF NOT EXISTS data_from_test_task (№ INTEGER, заказ_№ INTEGER, стоимость_руб REAL, срок_поставки DATE)")


def sql_add_line(values, values1, values2, values3):
    """
    Добавляем строку в БД, если добавили новую строку в GoogleSheet
    :param values: Порядковый номер
    :param values1: Номер заказа
    :param values2: Стоимость
    :param values3: Срок доставки
    """
    sql_execute("INSERT INTO data_from_test_task VALUES (%s, %s, '%s', '%s')" % (values, values1, values2, values3))


def sql_delete_task(value):
    """
    Удаляем строку из БД (определённого номера заказа)
    :param value: Номер заказа.
    """
    sql_execute("DELETE FROM data_from_test_task WHERE заказ_№ = %s" % value)


def sql_get_select_all_data():
    """
    Возвращает данные из БД.
    :return: Данне из таблицы в виде вложенных списков
    """
    conn = psycopg2.connect(key_psycopg2_connect)
    cur = conn.cursor()
    select_data = "SELECT * FROM data_from_test_task"
    cur.execute(select_data)
    data_sheets = cur.fetchall()
    return data_sheets

