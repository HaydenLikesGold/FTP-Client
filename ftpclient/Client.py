from socket import *

import login
import lifecycle


def get_server_response_less_basic():
    global _clientSocket
    global _createdSocket
    global _socketFile
    global _createdFile

    _clientSocket = socket(SOCK_DGRAM)
    _createdSocket = socket(SOCK_DGRAM)
    _socketFile = _clientSocket.makefile(mode="rw")
    _createdFile = _createdSocket.makefile(mode="rw")

    lifecycle.connect_to_princeton_server(_socketFile, _clientSocket)
    login.user_login_process(_socketFile)
    lifecycle.connect_to_new_socket(_createdSocket, _socketFile)
    data = lifecycle.retrieve_data(_socketFile, _createdFile)

    lifecycle.close_server_connection(_socketFile)
    return data


print(get_server_response_less_basic())
