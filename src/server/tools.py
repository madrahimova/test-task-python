"""
Упрощение работы с запросами
"""
import re
import api


def make_response(code: int, content: str) -> str:
    return f'HTTP/1.0 {code}\nAccess-Control-Allow-Origin: *\n\n{content}'


def handle_endpoint(endpoint: str, data=None):
    if endpoint == '/':
        return make_response(200, '')
    elif re.match(r'^/users$', endpoint):
        return make_response(200, api.users())
    elif re.match(r'^/users/add$', endpoint):
        return make_response(200, api.add_user(data))
    elif re.match(r'^/regions$', endpoint):
        return make_response(200, api.regions())
    elif re.match(r'^/cities\?region=\d+$', endpoint):
        return make_response(200, api.cities(endpoint))
    elif re.match(r'^/import/excel$', endpoint):
        return make_response(200, api.import_excel(data))
    elif re.match(r'^/export/excel$', endpoint):
        return make_response(200, api.export_excel())
    elif re.match(r'^/import/pdf$', endpoint):
        return make_response(200, api.import_pdf(data))
    elif re.match(r'^/export/pdf$', endpoint):
        return make_response(200, api.export_pdf())
    return make_response(404, '404 Not Found')

