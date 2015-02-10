import ftp_response_handler
import response

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
    socket_file.write('PASV\r\n')
    socket_file.flush()
    new_port_information = response.get_response(socket_file)
    validate_pasv_and_quit_command(new_port_information)
    return response.response_to_port_tuple(new_port_information)


def validate_pasv_and_quit_command(response):
    ftp_response_handler.raise_ftp_error_for_values(response, [1, 3])
    ftp_response_handler.raise_ftp_failure_for_values(response, [4, 5])
    ftp_response_handler.raise_error_if_not_in_given_values(response, [2])


def send_retr_command(socket_file):
    socket_file.write('RETR /pub/cs126/nbody/3body.txt\r\n')
    socket_file.flush()
    validate_retr_command(response.get_response(socket_file))
    validate_retr_command(response.get_response(socket_file))


def validate_retr_command(response):
    ftp_response_handler.raise_ftp_error_for_values(response, [3])
    ftp_response_handler.raise_ftp_failure_for_values(response, [4, 5])
    ftp_response_handler.raise_error_if_not_in_given_values(response, [1, 2])


def retrieve_data(socket_file, created_file):
    send_retr_command(socket_file)
    return response.get_retr_response(created_file)


def close_server_connection(socket_file):
    socket_file.write('QUIT\r\n')
    socket_file.flush()
    validate_pasv_and_quit_command(response.get_response(socket_file))
