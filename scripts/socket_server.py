import socket


def myServer(host='127.0.0.1', port=9000):
    so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    so.bind((host, port))
    so.listen(5)

    while True:
        conn, addr = so.accept()
        print("Connected by {}".format(addr))
        conn.send(b"ok\n")
        while 1:
            data = conn.recv(1024)
            # if not data: break
            conn.sendall(data)


if __name__ == '__main__':
    _HOST = "0.0.0.0"
    _PORT = 9000
    myServer(_HOST, _PORT)
