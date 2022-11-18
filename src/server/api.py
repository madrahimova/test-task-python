"""
Обработка запросов
"""
import base64
import json
import os
import PyPDF2
import openpyxl
import fpdf
import db


def __ids_to_names(user, _regions, _cities):
    for region in _regions:
        if user['region_id'] == region['id']:
            user['region_id'] = region['region_name']
    for city in _cities:
        if user['city_id'] == city['id']:
            user['city_id'] = city['city_name']
    return user


def __name_to_id(value, _regions, _cities):
    for region in _regions:
        if value == region['region_name']:
            value = region['id']
    for city in _cities:
        if value == city['city_name']:
            value = city['id']
    return value


def __replace_invalid(user, _regions, _cities):
    if user['region_id'] not in [item['id'] for item in _regions]:
        user['region_id'] = ''
    if user['city_id'] not in [item['id'] for item in _cities]:
        user['city_id'] = ''
    for k in user:
        if user[k] is None:
            user[k] = ''
    return user


def users():
    conn = db.connect('../db.sqlite')
    _users = db.select(conn, 'users')
    _regions = db.select(conn, 'regions')
    _cities = db.select(conn, 'cities')

    for i in range(len(_users)):
        _users[i] = __replace_invalid(_users[i], _regions, _cities)

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


def import_excel(data):
    columns = ['second_name', 'first_name', 'patronymic', 'region_id', 'city_id', 'phone', 'email']
    tmp_path = 'tmp.xlsx'

    with open(tmp_path, 'wb') as f:
        f.write(data)

    try:
        workbook = openpyxl.load_workbook(tmp_path)
    except:
        os.remove(tmp_path)
        return json.dumps({'body': 'ERR'})
    os.remove(tmp_path)

    sheet = workbook.active
    conn = db.connect('../db.sqlite')
    _users = db.select(conn, 'users')
    _regions = db.select(conn, 'regions')
    _cities = db.select(conn, 'cities')

    db.delete_from(conn, 'users')
    for row in sheet.iter_rows(min_row=2, min_col=2):
        values = []
        for cell in row:
            value = __name_to_id(cell.value, _regions, _cities)
            if value is None:
                value = ''
            values.append(value)
        try:
            db.insert(conn, 'users', columns, values)
        except:
            db.insert(conn, 'users', columns, _users)
            return json.dumps({'body': 'ERR'})

    conn.close()
    return json.dumps({'body': 'OK'})


def export_excel():
    columns = {'id': 'id', 'second_name': 'Фамилия', 'first_name': 'Имя', 'patronymic': 'Отчество',
              'region_id': 'Регион', 'city_id': 'Город',
              'phone': 'Контактный телефон', 'email': 'e-mail'}
    tmp_path = 'tmp.xlsx'

    conn = db.connect('../db.sqlite')
    _users = db.select(conn, 'users')
    _regions = db.select(conn, 'regions')
    _cities = db.select(conn, 'cities')
    conn.close()

    for i in range(len(_users)):
        _users[i] = __replace_invalid(_users[i], _regions, _cities)
        _users[i] = __ids_to_names(_users[i], _regions, _cities)
        _users[i] = {columns[column]: _users[i][column] for column in columns}

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(list(columns.values()))
    for user in _users:
        sheet.append(list(user.values()))
    workbook.save(tmp_path)

    with open(tmp_path, 'rb') as f:
        data = f.read()
        f.close()
    os.remove(tmp_path)
    return base64.b64encode(data)


def import_pdf(data):
    columns = ['second_name', 'first_name', 'patronymic', 'region_id', 'city_id', 'phone', 'email']
    tmp_path = 'tmp.pdf'

    with open(tmp_path, 'wb') as f:
        f.write(data)

    f = open('tmp.pdf', 'rb')
    os.remove(tmp_path)

    try:
        reader = PyPDF2.PdfFileReader(f)
    except:
        return json.dumps({'body': 'ERR'})

    conn = db.connect('../db.sqlite')
    _users = db.select(conn, 'users')
    _regions = db.select(conn, 'regions')
    _cities = db.select(conn, 'cities')

    db.delete_from(conn, 'users')
    for i in range(reader.getNumPages()):
        pdf = reader.getPage(i)
        lines = pdf.extractText().split('\n')
        full_name = lines[0].split(' ')
        values = [item for item in full_name]
        for j in range(1, len(lines)):
            values.append(lines[j].split(': ')[1])
        values = [__name_to_id(values[i], _regions, _cities) for i in range(len(values))]
        try:
            db.insert(conn, 'users', columns, values)
        except:
            db.insert(conn, 'users', columns, _users)
            json.dumps({'body': 'ERR'})

    conn.close()
    return json.dumps({'body': 'OK'})


def export_pdf():
    tmp_path = 'tmp.pdf'

    conn = db.connect('../db.sqlite')
    _users = db.select(conn, 'users')
    _regions = db.select(conn, 'regions')
    _cities = db.select(conn, 'cities')
    conn.close()

    pdf = fpdf.FPDF(format='letter')
    pdf.add_font('DejaVu', '', '../res/DejaVuSansCondensed.ttf', uni=True)
    for i in range(len(_users)):
        _users[i] = __ids_to_names(_users[i], _regions, _cities)
        pdf.add_page()
        pdf.set_font('DejaVu', '', 20)
        pdf.cell(200, 20, txt='%s %s %s' % (_users[i]['second_name'], _users[i]['first_name'], _users[i]['patronymic']),
                 ln=1, align='C')
        pdf.set_font('DejaVu', '', 14)
        pdf.cell(200, 10, txt='Регион: %s' % _users[i]['region_id'], ln=4, align='L')
        pdf.cell(200, 10, txt='Город: %s' % _users[i]['city_id'], ln=5, align='L')
        pdf.cell(200, 10, txt='Контактный телефон: %s' % _users[i]['phone'], ln=2, align='L')
        pdf.cell(200, 10, txt='e-mail: %s' % _users[i]['email'], ln=3, align='L')
    pdf.output(tmp_path)

    with open(tmp_path, 'rb') as f:
        data = f.read()
        f.close()
    os.remove(tmp_path)
    return base64.b64encode(data)


