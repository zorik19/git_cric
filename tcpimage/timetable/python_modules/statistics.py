from . import constant
from . import toi_connect


def send_board(command, sock, buffer):
    data_asc = command.encode()
    data_hex = data_asc.fromhex(command)
    print('data_hex', data_hex)
    sock.send(data_hex)
    resp = sock.recv(buffer)
    return resp


def statistic(command_1, command_2):
    main_socket = toi_connect.sock_connect(buffer=16603)
    toi_connect.send_board(command=constant.login_T30, sock=main_socket, buffer=4096)

    resp = send_board(command=command_1, sock=main_socket, buffer=8192)
    print(resp)
    resp = send_board(command=command_2, sock=main_socket, buffer=64)
    resp = str(resp)
    print(resp)
    value_split = resp.split(sep="value", maxsplit=2)
    print(value_split[1][2:-4])
    return value_split[1][2:-4]


def main():
    command_1 = '41564f4e0a00000051522100050400000000000000000b02'
    command_2 = '41564f4e0c00000051522100050100000000000000000a0241564f4e0d00000051521a000500000000000000000003' \
                '0241564f4e0b00000051522100050300000000000000000b02'
    final = statistic(command_1, command_2)
    return final


if __name__ == "__main__":
    #test = sys.argv[1]
    main()

