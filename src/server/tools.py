"""
Упрощение работы с запросами
"""
from . import api


def make_response(code: int, content: str) -> str:
    return f'HTTP/1.0 {code}\nAccess-Control-Allow-Origin: *\n\n{content}'


def handle_endpoint(endpoint: str):
    if endpoint == '/':
        return make_response(200, '')
    elif endpoint.startswith('/users'):
        return make_response(200, api.users())
    elif endpoint.startswith('/regions'):
        return make_response(200, api.regions())
    elif endpoint.startswith('/cities'):
        return make_response(200, api.cities(endpoint))
    return make_response(404, '404 Not Found')

