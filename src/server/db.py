"""
Работа с базой данных
"""
import sqlite3
from sqlite3 import Error


def connect(db):
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    return conn


def select(conn, table: str, cond=None):
    cur = conn.cursor()
    cur.execute('SELECT * FROM %s %s' % (table, f'WHERE {cond}' if cond else ''))
    columns, rows = __get_columns(conn, table), cur.fetchall()
    for i in range(len(rows)):
        rows[i] = {columns[j]: rows[i][j] for j in range(len(rows[i]))}
    return rows


def __get_columns(conn, table):
    cur = conn.execute(f'SELECT * FROM %s' % table)
    return [desc[0] for desc in cur.description]


def insert(conn, table: str, columns: list, values: list):
    cur = conn.cursor()
    params = ','.join(['?' for _ in values])
    cur.execute(f'INSERT INTO {table} ({",".join([item for item in columns])}) VALUES ({params})',
                [str(item) for item in values])
    conn.commit()
