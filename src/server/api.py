"""
Обработка запросов
"""
import json
from . import db


def users():
    conn = db.connect('../db.sqlite')
    result = json.dumps({'body': db.select(conn, 'users')})
    conn.close()
    return result


def regions():
    conn = db.connect('../db.sqlite')
    result = json.dumps({'body': db.select(conn, 'regions')})
    conn.close()
    return result


def cities(endpoint: str = None):
    cond = ''
    try:
        cond = endpoint.split('/')[1].split('=')[1]
    except IndexError:
        pass
    conn = db.connect('../db.sqlite')
    result = json.dumps({'body': db.select(conn, 'cities', f'cities.region_id = {cond}')})
    conn.close()
    return result
