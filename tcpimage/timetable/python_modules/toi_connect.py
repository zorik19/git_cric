from . import constant
import socket


def sock_connect(buffer):
    sock = socket.socket()
    sock.connect((constant.hostIP, buffer))
    return sock


def send_board(command, sock, buffer):
    data_asc = command.encode()

    data_hex = data_asc.fromhex(command)
    print(data_hex)
    sock.send(data_hex)
    resp = sock.recv(buffer)
    return sock


def send_board_test(command):
    sock = sock_connect(5200)
    data_asc = command.encode()
    data_hex = data_asc.fromhex(command)
    print('data_hex', data_hex)
    sock.send(data_hex)
    resp = sock.recv(5200)
    print(resp)


def send_board_mon(command, sock, buffer):
    data_asc = command.encode()

    data_hex = data_asc.fromhex(command)
    print(data_hex)
    sock.send(data_hex)
    resp = sock.recv(buffer)
    return resp