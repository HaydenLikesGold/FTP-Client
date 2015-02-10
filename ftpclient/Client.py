from socket import *

import ftp_response_handler
import response

# Login Process
def user_login_process():
    user_response_code = user_entry()
    if (user_response_code == 3):
        pass_response_code = password_entry()
        if (pass_response_code == 3):
            acct_entry()


def user_entry():
    _socketFile.write("USER anonymous\r\n")
    _socketFile.flush()
    response_x = response.get_response(_socketFile)
    validate_user_and_pass_response(response_x)
    return int(response_x[0:1])


def password_entry():
    _socketFile.write('PASS anonymous@gustavus.edu\r\n')
    _socketFile.flush()
    pass_response = response.get_response(_socketFile)
    validate_user_and_pass_response(pass_response)
    return int(pass_response[0:1])


def validate_user_and_pass_response(response):
    ftp_response_handler.raise_ftp_error_for_values(response, [1])
    ftp_response_handler.raise_ftp_failure_for_values(response, [4, 5])
    ftp_response_handler.raise_error_if_not_in_given_values(response, [2, 3])


def acct_entry():
    _socketFile.write('ACCT anonymous\r\n')
    _socketFile.flush()
    acct_response = response.get_response(_socketFile)
    validate_acct_response(acct_response)


def validate_acct_response(response):
    ftp_response_handler.raise_ftp_error_for_values(response, [1, 3])
    ftp_response_handler.raise_ftp_failure_for_values(response, [4, 5])
    ftp_response_handler.raise_error_if_not_in_given_values(response, [2])


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
    user_login_process()
    connect_to_new_socket()
    data = retrieve_data()

    close_server_connection()
    return data


print(get_server_response_less_basic())
