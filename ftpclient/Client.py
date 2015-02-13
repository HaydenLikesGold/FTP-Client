from socket import *

import login
import lifecycle


def get_server_response_less_basic():
    client_socket = socket(SOCK_DGRAM)
    created_socket = socket(SOCK_DGRAM)
    socket_file = client_socket.makefile(mode="rw")
    created_file = created_socket.makefile(mode="rw")

    lifecycle.connect_to_princeton_server(socket_file, client_socket)
    login.user_login_process(socket_file)
    lifecycle.connect_to_new_socket(created_socket, socket_file)
    data = lifecycle.retrieve_data(socket_file, created_file)

    lifecycle.close_server_connection(socket_file)
    return data


print(get_server_response_less_basic())
