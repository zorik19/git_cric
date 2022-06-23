from . import constant
from . import toi_connect


def testing(command_test):
    sock = toi_connect.sock_connect(buffer=16603)
    buffer = 4096
    login = toi_connect.send_board(constant.login_T30, sock, buffer)

    # connection session
    toi_connect.send_board(command=constant.login_session, sock=login, buffer=1024)

    sock_5200 = toi_connect.sock_connect(buffer=5200)
    toi_connect.send_board(command_test, sock_5200, buffer)


def main(com):
    a = toi_connect.sock_connect(buffer=16603)
    testing(com)
    print(a)


if __name__ == "__main__":
    # test = sys.argv[1]
    test = 'vertical'
    print(test)

    main(test)

