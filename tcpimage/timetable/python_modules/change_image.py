import os
import hashlib
import shutil
from . import constant, toi_connect
import logging


class UpdateImage:

    def __init__(self, image_list):
        self.source_path = os.path.join(constant.path_for_image, 'timetable/python_modules/source/')
        self.media_path = os.path.join(constant.path_for_image, 'media')
        self.out_path = os.path.join(constant.path_for_image, 'timetable/python_modules/source/output/')
        self.input_image_list = image_list

    def run(self):
        self.create_custom_json()

        main_socket = toi_connect.sock_connect(buffer=16603)
        toi_connect.send_board(command=constant.login_T30, sock=main_socket, buffer=4096)

        # socket for ftp transfer
        socket_ftp = toi_connect.sock_connect(buffer=16602)

        # transfer json`s to board
        self.apply_ftp_command(sock=socket_ftp)

        for json_item in constant.list_json:
            json_path = constant.program_path_ftp + json_item + "\n"
            self.ftp_transfer(socket_ftp=socket_ftp, file_name=json_item, path_file=json_path)

        for image_item in self.input_image_list:
            in_image_path = os.path.join(self.media_path, image_item)
            md5_hash = self.calculate_md5_hash_image(in_image_path)
            out_image_path = os.path.join(self.out_path, image_item)

            # copy image with same name
            shutil.copyfile(in_image_path, out_image_path)

            # copy image with md5 name
            md5output_path = self.source_path + '/output/' + md5_hash + '.png'
            shutil.copyfile(in_image_path, md5output_path)

            # transfer image to project folder ftp
            path_project = constant.program_path_ftp + md5_hash + ".png\n"
            self.ftp_transfer(socket_ftp=socket_ftp, file_name=image_item, path_file=path_project)

            # transfer image to media folder ftp
            path_media = constant.media_path_ftp + md5_hash + ".png\n"
            self.ftp_transfer(socket_ftp=socket_ftp, file_name=image_item, path_file=path_media)

        # activate project
        toi_connect.send_board(command=constant.activate_change_image, sock=main_socket, buffer=1024)

    def ftp_transfer(self, socket_ftp, file_name: str, path_file: str) -> None:
        passive_session_ftp = "PASV\n".encode()
        socket_ftp.sendall(passive_session_ftp)

        buffer_size = self.calculate_buffer_size(str(socket_ftp.recv(128)))

        socket_ftp.sendall(path_file.encode())
        socket_ftp.recv(128)

        new_socket = toi_connect.sock_connect(buffer=buffer_size)

        if '.json' in file_name:
            path_to_finished_json = os.path.join(self.out_path, file_name)
            finished_json = open(path_to_finished_json, 'rb')
            file_size = os.path.getsize(path_to_finished_json)
            data = finished_json.read(file_size)
            new_socket.send(data)
            new_socket.close()
        else:
            f = open(self.source_path + '/output/' + file_name, 'rb')
            while True:
                line = f.readline(512)
                if not line:
                    break
                new_socket.send(line)
            new_socket.close()
        an = socket_ftp.recv(1024)
        print('final send_json_to_board:', an)

    @staticmethod
    def calculate_buffer_size(value: str) -> int:
        value_split = value.split(sep=",", maxsplit=5)
        value_split_2 = str(value_split[5]).find(")")
        port_value = int(value_split[4]) * 256 + int(value_split[5][0:value_split_2])
        return port_value

    @staticmethod
    def apply_ftp_command(sock) -> None:
        sock.recv(1024)
        for command in constant.list_plat:
            data = command.encode()
            sock.sendall(data)
            h = sock.recv(1024)
            print(h)

    @staticmethod
    def calculate_md5_hash_image(image_path: str) -> str:
        pic = open(image_path, 'rb')
        data = pic.read()
        tmp_md5 = hashlib.md5(data)
        md5 = tmp_md5.hexdigest()
        pic.close()
        return md5

    def create_custom_json(self) -> None:
        md5_list = []
        pic_size_list = []
        for file in self.input_image_list:
            in_image = os.path.join(self.media_path, file)
            md5 = self.calculate_md5_hash_image(in_image)
            md5_list.append(md5)
            pic_size = os.path.getsize(in_image)
            pic_size_list.append(pic_size)

        self.clear_output_catalog()
        for json_item in constant.list_json:
            path_out = os.path.join(self.out_path, json_item)
            i = 1
            if 'plan' in json_item:
                path_in = os.path.join(self.source_path, constant.list_change_json1[len(md5_list) - 1])
                print(path_in)
                with open(path_out, 'w') as finish_json:
                    with open(path_in, 'r', encoding='utf8') as start_json:
                        for line in start_json:
                            if i == 34:
                                line = ' '*6 + '\"fileName\": \"' + md5_list[0] + '.png\",\n'
                            if i == 35:
                                line = ' '*6 + '\"md5\": \"' + md5_list[0] + '\",\n'
                            if i == 37:
                                line = ' '*6 + '"size": ' + str(pic_size_list[0]) + '\n'

                            if len(md5_list) == 2 or len(md5_list) == 3:
                                if i == 40:
                                    line = ' '*6 + '\"fileName\": \"' + md5_list[1] + '.png\",\n'
                                if i == 41:
                                    line = ' '*6 + '\"md5\": \"' + md5_list[1] + '\",\n'
                                if i == 43:
                                    line = ' '*6 + '"size": ' + str(pic_size_list[1]) + '\n'
                            if len(md5_list) == 3:
                                if i == 46:
                                    line = ' '*6 + '\"fileName\": \"' + md5_list[2] + '.png\",\n'
                                if i == 47:
                                    line = ' '*6 + '\"md5\": \"' + md5_list[2] + '\",\n'
                                if i == 49:
                                    line = ' '*6 + '"size": ' + str(pic_size_list[2]) + '\n'
                            finish_json.write(line)
                            i += 1
            elif 'playlist' in json_item:
                path_in = os.path.join(self.source_path, constant.list_change_json2[len(md5_list) - 1])
                with open(path_out, 'w') as finish_json:
                    with open(path_in, 'r', encoding='utf8') as start_json:
                        for line in start_json:
                            if i == 94:
                                line = ' '*18 + "\"filesize\": " + str(pic_size_list[0]) + ",\n"
                            if i == 97:
                                line = ' '*18 + "\"dataSource\": \"" + md5_list[0] + ".png\",\n"
                            if i == 101:
                                line = ' '*18 + "\"name\": \"" + self.input_image_list[0] + "\",\n"

                            if len(md5_list) == 2:
                                if i == 233:
                                    line = ' '*18 + "\"filesize\": " + str(pic_size_list[1]) + ",\n"
                                if i == 236:
                                    line = ' '*18 + "\"dataSource\": \"" + md5_list[1] + ".png\",\n"
                                if i == 240:
                                    line = ' '*18 + "\"name\": \"" + self.input_image_list[1] + "\",\n"

                            if len(md5_list) == 3:
                                if i == 232:
                                    line = ' '*18 + "\"filesize\": " + str(pic_size_list[1]) + ",\n"
                                if i == 235:
                                    line = ' '*18 + "\"dataSource\": \"" + md5_list[1] + ".png\",\n"
                                if i == 239:
                                    line = ' '*18 + "\"name\": \"" + self.input_image_list[1] + "\",\n"

                                if i == 371:
                                    line = ' '*18 + "\"filesize\": " + str(pic_size_list[2]) + ",\n"
                                if i == 374:
                                    line = ' '*18 + "\"dataSource\": \"" + md5_list[2] + ".png\",\n"
                                if i == 378:
                                    line = ' '*18 + "\"name\": \"" + self.input_image_list[2] + "\",\n"
                            finish_json.write(line)
                            i += 1
            else:
                path_in = os.path.join(self.source_path, json_item)
                path_out = os.path.join(self.out_path, json_item)
                shutil.copyfile(path_in, path_out)

    def clear_output_catalog(self) -> None:
        for file_object in os.listdir(self.out_path):
            file_object_path = os.path.join(self.out_path, file_object)
            if os.path.isfile(file_object_path):
                os.unlink(file_object_path)
            else:
                shutil.rmtree(file_object_path)


def main(image_list):
    try:
        update = UpdateImage(image_list)
        update.run()
        print("Change image success")
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        print(e)


if __name__ == "__main__":
    print('in')
