import os
import sys
import socket
import time
import multiprocessing

HOST = ''
PORT = 8080

def worker(conn, addr):
    with conn:
        print(f'Connected by {addr}')
        data = conn.recv(1500)
        ptr = data.find('\r\n'.encode('utf-8'))
        header = data[:ptr]
        left = data[ptr:]
        request = header.decode('utf-8')
        method, path, protocol = request.split(' ')
        print(f'Received: {method} {path} {protocol}')
        if not data:
            raise KeyboardInterrupt
        if path == '/':
            path = '/index.html'
        path = f'.{path}'
        if not os.path.exists(path):
            header = 'HTTP/1.1 404 Not Found\r\n'
            header = f'{header}Server: Our server\r\n'
            header = f'{header}Connection: close\r\n'
            header = f'{header}Content-Type: text/html;charset=utf-8\r\n'
            header = f'{header}\r\n'
            header = header.encode('utf-8')
            body = ''.encode('utf-8')
        else:
            if path.endswith(".jpg") | path.endswith(".png"):
                with open(path, 'rb') as f:
                    body = f.read()
            else:
                with open(path, 'r', encoding='utf-8') as f:
                    body = f.read()
                    body = body.encode('utf-8')
            
            header = 'HTTP/1.1 200 OK\r\n'
            header = f'{header}Server: Our server\r\n'
            header = f'{header}Connection: close\r\n'

            if path.endswith(".html"):
                header = f'{header}Content-Type: text/html;charset=utf-8\r\n'
            elif path.endswith(".css"):
                header = f'{header}Content-Type: text/css;charset=utf-8\r\n'
            elif path.endswith(".js"):
                header = f'{header}Content-Type: text/javascript;charset=utf-8\r\n'
            elif path.endswith(".jpg"):
                header = f'{header}Content-Type: image/jpeg;charset=utf-8\r\n'
            elif path.endswith(".png"):
                header = f'{header}Content-Type: image/png;charset=utf-8\r\n'

            header = f'{header}Content-Length: {len(body)}\r\n'
            header = f'{header}\r\n'
            header = header.encode('utf-8')
        response = header + body
        conn.sendall(response)
        conn.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1024)
    print(f'Start server with {sys.argv}')
    while True:
        try:
            conn, addr = s.accept()
            process = multiprocessing.Process(target=worker,
                                              args=(conn, addr))
            process.start()
            print(f'Start child worker {process}')
        except KeyboardInterrupt:
            print('Shutdown server')
            for process in multiprocessing.active_children():
                print('Terminate process {0}'.format(process))
                process.terminate()
                process.join()
            break

