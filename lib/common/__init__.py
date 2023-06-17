import socket


def check_port(port: int):
    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        Socket.connect(("127.0.0.1", port))
        return False
    except:
        return True
