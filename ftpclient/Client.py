from socket import *

import login
import lifecycle


def get_server_response_less_basic():
    clientSocket = socket(SOCK_DGRAM)
    createdSocket = socket(SOCK_DGRAM)
    socketFile = clientSocket.makefile(mode="rw")
    createdFile = createdSocket.makefile(mode="rw")

    lifecycle.connect_to_princeton_server(socketFile, clientSocket)
    login.user_login_process(socketFile)
    lifecycle.connect_to_new_socket(createdSocket, socketFile)
    data = lifecycle.retrieve_data(socketFile, createdFile)

    lifecycle.close_server_connection(socketFile)
    return data


print(get_server_response_less_basic())
