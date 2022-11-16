"""
Упрощение работы с запросами
"""
import socket


def port_lookup() -> int:
    for port in range(3000, 60000):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if server.connect_ex(('127.0.0.1', port)) == 0:
            server.close()
            return port
        server.close()
    raise Exception('Open port not found')


def make_response(code: int, content: str) -> str:
    return f'HTTP/1.0 {code}\n\n{content}'


def handle_endpoint(endpoint: str) -> str:
    if endpoint == '/':
        return make_response(200, '')
    return make_response(404, '404 Not Found')

