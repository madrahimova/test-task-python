from server.tools import port_lookup, handle_endpoint
import socket


def run():
    host, port = '127.0.0.1', port_lookup()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(1)
    print(f'Listening on http://{host}:{port}')
    while True:
        client, addr = server.accept()
        request = client.recv(1024).decode()
        endpoint = request.split('\n')[0].split(' ')[1]
        response = handle_endpoint(endpoint)
        client.sendall(response.encode())
        client.close()

    server.close()


run()
