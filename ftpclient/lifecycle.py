import ftp_response_handler
import response


PASV_COMMAND = 'PASV\r\n'
QUIT_COMMAND = 'QUIT\r\n'


class Lifecycle:
    def __init__(self, server, port, file_path, socket_file, client_file):
        self.server_name = server
        self.server_port = port
        self.retr_command = 'RETR ' + file_path + '\r\n'
        self.socket_file = socket_file
        self.client_file = client_file

    def connect_to_server(self, client_socket):
        client_socket.connect((self.server_name, self.server_port))
        client_socket.close()
        response.get_response(self.socket_file)

    def connect_to_new_socket(self, socket):
        pasv_port = self.send_pasv_command()
        socket.connect(pasv_port)
        socket.close()

    def send_pasv_command(self):
        new_port_information = response.get_response(self.socket_file,
                                                     PASV_COMMAND)
        ftp_response_handler.validate_pasv_and_quit_command(
            new_port_information)
        return response.response_to_port_tuple(new_port_information)

    def send_retr_command(self):
        ftp_response_handler.validate_retr_command(
            response.get_response(self.socket_file, self.retr_command))
        ftp_response_handler.validate_retr_command(
            response.get_response(self.socket_file))

    def retrieve_data(self):
        self.send_retr_command()
        return response.get_retr_response(self.client_file)

    def close_server_connection(self):
        ftp_response_handler.validate_pasv_and_quit_command(
            response.get_response(self.socket_file, QUIT_COMMAND))
