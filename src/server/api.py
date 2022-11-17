"""
Обработка запросов
"""
import json
from . import db


def users():
    conn = db.connect('../db.sqlite')
    _users = db.select(conn, 'users')
    _regions = db.select(conn, 'regions')
    _cities = db.select(conn, 'cities')

    for i in range(len(_users)):
        if _users[i]['region_id'] not in [item['id'] for item in _regions]:
            _users[i]['region_id'] = ''

    for i in range(len(_users)):
        if _users[i]['city_id'] not in [item['id'] for item in _cities]:
            _users[i]['city_id'] = ''

    result = json.dumps({'body': _users})
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


def add_user(data):
    conn = db.connect('../db.sqlite')
    db.insert(conn, 'users', data.keys(), data.values())
    conn.close()
    return json.dumps({'body': 'OK'})
