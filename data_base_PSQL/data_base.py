import psycopg2
from config_project.config import key_psycopg2_connect  # Импортируем подключение к PostgresSQL

# =========================================== БД ===============================================


def sql_start():
    conn = psycopg2.connect(key_psycopg2_connect)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS data_from_test_task (№ INTEGER PRIMARY KEY, заказ_№ INTEGER, стоимость_руб REAL, срок_поставки DATE)")
    conn.commit()
    print('The database is connected!')
    conn.close()


def sql_add_line(values, values1, values2, values3):
    conn = psycopg2.connect(key_psycopg2_connect)
    cur = conn.cursor()
    cur.execute("INSERT INTO data_from_test_task VALUES (%s, %s, '%s', '%s')" % (values, values1, values2, values3))
    conn.commit()
    conn.close()


def sql_delete_task(value):
    """
    Функция удаляем строку из БД (определённого номера заказа)
    :param value: Номер заказа.
    """
    conn = psycopg2.connect(key_psycopg2_connect)
    cur = conn.cursor()
    cur.execute("DELETE FROM data_from_test_task WHERE заказ_№ = %s" % value)
    conn.commit()
    conn.close()


def sql_get_select_all_data():
    """
    Функция, которая заглядывает в БД и берёт все данные таблицы.
    :return: Данне из таблицы в виде вложенных списков
    """
    conn = psycopg2.connect(key_psycopg2_connect)
    cur = conn.cursor()
    select_data = "SELECT * FROM data_from_test_task"
    cur.execute(select_data)
    data_sheets = cur.fetchall()
    return data_sheets

