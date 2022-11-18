"""
Упрощение работы с запросами
"""
import api


def make_response(code: int, content: str) -> str:
    return f'HTTP/1.0 {code}\nAccess-Control-Allow-Origin: *\n\n{content}'


def handle_endpoint(endpoint: str, data=None):
    if endpoint == '/':
        return make_response(200, '')
    elif endpoint.startswith('/users/add'):
        return make_response(200, api.add_user(data))
    elif endpoint.startswith('/users'):
        return make_response(200, api.users())
    elif endpoint.startswith('/regions'):
        return make_response(200, api.regions())
    elif endpoint.startswith('/cities'):
        return make_response(200, api.cities(endpoint))
    elif endpoint.startswith('/import/excel'):
        return make_response(200, api.import_excel(data))
    elif endpoint.startswith('/export/excel'):
        return make_response(200, api.export_excel())
    elif endpoint.startswith('/import/pdf'):
        return make_response(200, api.import_pdf(data))
    elif endpoint.startswith('/export/pdf'):
        return make_response(200, api.export_pdf())
    return make_response(404, '404 Not Found')

