from server.tools import handle_endpoint
import socket
import subprocess


def run():
    host, port = '127.0.0.1', 12345
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(1)
    print(f'Server is listening on http://{host}:{port}')
    while True:
        client, addr = server.accept()
        request = client.recv(1024).decode()
        method, endpoint, _ = request.split('\n')[0].split(' ')
        response = 'HTTP/1.0 405\n\nMethod Not Allowed'
        if method == 'POST':
            response = handle_endpoint(endpoint)
        client.sendall(response.encode())
        client.close()

    server.close()


try:
    open('../db.sqlite').close()
except FileNotFoundError:
    open('../db.sqlite', 'x').close()
    subprocess.call(['sh', './db.sh'], cwd='../')

run()
