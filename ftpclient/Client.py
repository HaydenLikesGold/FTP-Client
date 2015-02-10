from socket import *

import ftp_response_handler
import response
import login

# Connection Process
def connect_to_princeton_server():
    serverName = 'ftp.cs.princeton.edu'
    serverPort = 21
    _clientSocket.connect((serverName, serverPort))
    _clientSocket.close()
    response.get_response(_socketFile)


def connect_to_new_socket():
    pasv_port = send_pasv_command()
    _createdSocket.connect(pasv_port)
    _createdSocket.close()


def send_pasv_command():
    _socketFile.write('PASV\r\n')
    _socketFile.flush()
    newPortInformation = response.get_response(_socketFile)
    validate_pasv_and_quit_command(newPortInformation)
    return response.response_to_port_tuple(newPortInformation)


def validate_pasv_and_quit_command(response):
    ftp_response_handler.raise_ftp_error_for_values(response, [1, 3])
    ftp_response_handler.raise_ftp_failure_for_values(response, [4, 5])
    ftp_response_handler.raise_error_if_not_in_given_values(response, [2])


def send_retr_command():
    _socketFile.write('RETR /pub/cs126/nbody/3body.txt\r\n')
    _socketFile.flush()
    validate_retr_command(response.get_response(_socketFile))
    validate_retr_command(response.get_response(_socketFile))


def validate_retr_command(response):
    ftp_response_handler.raise_ftp_error_for_values(response, [3])
    ftp_response_handler.raise_ftp_failure_for_values(response, [4, 5])
    ftp_response_handler.raise_error_if_not_in_given_values(response, [1, 2])


def retrieve_data():
    send_retr_command()
    return response.get_retr_response(_createdFile)


def close_server_connection():
    _socketFile.write('QUIT\r\n')
    _socketFile.flush()
    validate_pasv_and_quit_command(response.get_response(_socketFile))


def get_server_response_less_basic():
    global _clientSocket
    global _createdSocket
    global _socketFile
    global _createdFile

    _clientSocket = socket(SOCK_DGRAM)
    _createdSocket = socket(SOCK_DGRAM)
    _socketFile = _clientSocket.makefile(mode="rw")
    _createdFile = _createdSocket.makefile(mode="rw")

    connect_to_princeton_server()
    login.user_login_process(_socketFile)
    connect_to_new_socket()
    data = retrieve_data()

    close_server_connection()
    return data


print(get_server_response_less_basic())
