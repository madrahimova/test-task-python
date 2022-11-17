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
    return cur.fetchall()
