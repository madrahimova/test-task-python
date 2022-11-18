import base64
import json
from tools import handle_endpoint, make_response
import socket
import subprocess
import os


def run():
    host, port = '127.0.0.1', 12345
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(1)
    print(f'Server is listening on http://{host}:{port}')
    while True:
        client, addr = server.accept()
        request = client.recv(1024 * 1024).decode('utf-8', 'ignore')
        method, endpoint, _ = request.split('\n')[0].split(' ')

        data = ''
        try:
            data = json.loads(request.split('\n')[-1])
        except json.decoder.JSONDecodeError: pass
        try:
            data = base64.b64decode(request.split('\n')[-1])
        except: pass

        if method == 'POST':
            response = handle_endpoint(endpoint, data)
        else:
            response = make_response(405, '405 Method Not Allowed')
        client.sendall(response.encode())
        client.close()

    server.close()


try:
    open('../db.sqlite').close()
except FileNotFoundError:
    open('../db.sqlite', 'x').close()
    src = os.path.dirname(__file__)
    parent = os.path.join(src, '../../')
    subprocess.call(['sh', os.path.join(parent, 'db.sh')], cwd='../')

run()
