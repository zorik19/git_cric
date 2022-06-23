from . import constant, toi_connect


class UpdateBright:

    def __init__(self, input_bright):
        self.input_bright = input_bright
        self.socket = toi_connect.sock_connect(buffer=16603)

    def set_bright(self):
        toi_connect.send_board(command=constant.login_T30, sock=self.socket, buffer=4096)
        if len(self.input_bright) == 1:
            self.input_bright = '0' + self.input_bright
        if self.input_bright != '100':
            data_byte = 'AVON%\x00\x00\x00QR\x18\x00\x04\x01\x00\x00\x0e\x00\x00\x00\x00\x00\'\x02{"ratio":' \
                     + self.input_bright + '.0}'
        else:
            data_byte = 'AVON\x16\x00\x00\x00QR\x18\x00\x04\x01\x00\x00\x0f\x00\x00\x00\x00\x00\x19\x02{"ratio":100.0}'
        data_byte = data_byte.encode()
        self.socket.send(data_byte)
        self.socket.recv(4096)
        self.socket.close()
        print('manual complete')


def main(input_bright):
    try:
        a = UpdateBright(input_bright=input_bright)
        a.set_bright()
        return 'done'

    except Exception as e:
        print(e)


if __name__ == "__main__":
    bright = '3'
    main(bright)

