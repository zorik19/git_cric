import socket

# chr_part_2 = bytearray(b'{"sn":"2021112610015504","username":"admin","password":"123456","loginType":3}')
# print(chr_part_2)
# hex_chr = chr_part_2.hex()
# print('hex_chr', hex_chr)
# reference_query_byte = bytearray.fromhex(com)
# print(reference_query_byte)
# f = bytes(data_hex)
# print(f, '888')
# sock.send(data_hex)
# resp = sock.recv(4096)
# print('resp', resp)
# return resp
hostIP = '192.168.0.100'
login_image = '7b22736e223a2232303230303830353830303035323733222c227' \
              '57365726e616d65223a2261646d696e222c2270617373776f7264223a22313233343536222c226c6f67696e54797065223a337d'

login_T30 = '41564f4e0100000051520000000000004e000000000026027b22736e223a2232303231313132363130303135353034222c2275' \
            '7365726e616d65223a2261646d696e222c2270617373776f7264223a22313233343536222c226c6f67696e54797065223a337d'
log2 = '41564f4e020000005152010005020000000000000000e101'

login_mon = '41564f4e0100000051520000000000004e000000000026027b22736e223a2232303230303830353830303035323733222c2275' \
             '7365726e616d65223a2261646d696e222c2270617373776f7264223a22313233343536222c226c6f67696e54797065223a337d'

login_mon_2 = '55aa0066fe000100ffff01000000001000010080800148140e2600808001501c1127058080018504072200808001501c11270' \
              '980800185040b2400808021300e8b24108080017c02040122808000850282003f800000240282003f80000024028200000000' \
              '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000808021300' \
              'e8b04108080017c02040122808000850282003f800000240282003f8000002402820000000000000000000000000000000000' \
              '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' \
              '00000000000000000000000000000000000000000003572'

login_mon_3 = '55aa0067fe000100ffff0100190000010b00af3f001b031b031b0301032b5a'

login_mon_4 = '55aa0068fe000100ffff010017000001010000d458'

login_mon_5 = '55aa0069fe0001000b000000000000020001cb56'

login_mon_6 = '55aa006afe0001000b000000000100020001cd56'

login_mon_7 = '55aa006bfe0001000b0000002000000a0100f556'

login_mon_8 = '55aa006cfe0001000b0000000000000380004e57'

login_mon_9 = '55aa006dfe0001000b0000008007000344009a57'
login_mon_1 = '55aa0065fe0001000b0000008d00000208005b57'
def sock_connect(buffer):
    sock = socket.socket()
    a = sock.connect((hostIP, buffer))
    print(a, 'sock_connect')
    return sock


def send_board(command):
    sock = sock_connect(16603)
    data_asc = command.encode()
    data_hex = data_asc.fromhex(command)
    print('data_hex11', data_hex)
    sock.send(data_hex)
    resp = sock.recv(5200)
    print(resp)
    return sock
# send_board(login_T30)
# send_board(log2)


def send_board2(command, sock, buffer):
    data_asc = command.encode()
    data_hex = data_asc.fromhex(command)
    # print('data_hex', data_hex)
    sock.send(data_hex)
    resp = sock.recv(buffer)
    print('999', resp)


p = send_board(login_T30)
sock = sock_connect(buffer=5200)
send_board2(login_mon_1, sock, buffer=92406)
send_board2(login_mon_2, sock, buffer=92406)
send_board2(login_mon_3, sock, buffer=92406)
send_board2(login_mon_4, sock, buffer=92406)
send_board2(login_mon_5, sock, buffer=92406)
send_board2(login_mon_6, sock, buffer=92406)
send_board2(login_mon_7, sock, buffer=92406)
send_board2(login_mon_8, sock, buffer=92406)
send_board2(login_mon_9, sock, buffer=92406)


