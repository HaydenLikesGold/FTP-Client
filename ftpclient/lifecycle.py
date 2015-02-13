import ftp_response_handler
import response


PASV_COMMAND = 'PASV\r\n'
RETR_COMMAND = 'RETR /pub/cs126/nbody/3body.txt\r\n'
QUIT_COMMAND = 'QUIT\r\n'


def connect_to_princeton_server(socket_file, client_socket):
    server_name = 'ftp.cs.princeton.edu'
    server_port = 21
    client_socket.connect((server_name, server_port))
    client_socket.close()
    response.get_response(socket_file)


def connect_to_new_socket(socket, socket_file):
    pasv_port = send_pasv_command(socket_file)
    socket.connect(pasv_port)
    socket.close()


def send_pasv_command(socket_file):
    new_port_information = response.get_response(socket_file, PASV_COMMAND)
    ftp_response_handler.validate_pasv_and_quit_command(new_port_information)
    return response.response_to_port_tuple(new_port_information)


def send_retr_command(socket_file):
    ftp_response_handler.validate_retr_command(
        response.get_response(socket_file, RETR_COMMAND))
    ftp_response_handler.validate_retr_command(
        response.get_response(socket_file))


def retrieve_data(socket_file, created_file):
    send_retr_command(socket_file)
    return response.get_retr_response(created_file)


def close_server_connection(socket_file):
    ftp_response_handler.validate_pasv_and_quit_command(
        response.get_response(socket_file, QUIT_COMMAND))
