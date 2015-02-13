from socket import *

import login
from lifecycle import Lifecycle


class FileTransfer:
    def __init__(self, server, port, file_path):
        self.server = server
        self.port = port
        self.file_path = file_path

    def ftp_process(self):
        client_socket = socket(SOCK_DGRAM)
        created_socket = socket(SOCK_DGRAM)
        socket_file = client_socket.makefile(mode="rw")
        created_file = created_socket.makefile(mode="rw")

        lifecycle = Lifecycle(self.server, self.port, self.file_path,
                              socket_file, created_file)
        lifecycle.connect_to_server(client_socket)
        login.user_login_process(socket_file)
        lifecycle.connect_to_new_socket(created_socket)
        response = lifecycle.retrieve_data()

        lifecycle.close_server_connection()
        print response
        return response



server_name = 'ftp.cs.princeton.edu'
server_port = 21
file_path = '/pub/cs126/nbody/3body.txt'

x = FileTransfer(server_name, server_port, file_path)
x.ftp_process()