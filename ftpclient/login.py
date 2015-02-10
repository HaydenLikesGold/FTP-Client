import ftp_response_handler
import response

def user_login_process(socket_file):
    user_response_code = user_entry(socket_file)
    if (user_response_code == 3):
        pass_response_code = password_entry(socket_file)
        if (pass_response_code == 3):
            acct_entry()

def user_entry(socket_file):
    socket_file.write("USER anonymous\r\n")
    socket_file.flush()
    response_x = response.get_response(socket_file)
    validate_user_and_pass_response(response_x)
    return int(response_x[0:1])


def password_entry(socket_file):
    socket_file.write('PASS anonymous@gustavus.edu\r\n')
    socket_file.flush()
    pass_response = response.get_response(socket_file)
    validate_user_and_pass_response(pass_response)
    return int(pass_response[0:1])


def validate_user_and_pass_response(response):
    ftp_response_handler.raise_ftp_error_for_values(response, [1])
    ftp_response_handler.raise_ftp_failure_for_values(response, [4, 5])
    ftp_response_handler.raise_error_if_not_in_given_values(response, [2, 3])


def acct_entry(socket_file):
    socket_file.write('ACCT anonymous\r\n')
    socket_file.flush()
    acct_response = response.get_response(socket_file)
    validate_acct_response(acct_response)


def validate_acct_response(response):
    ftp_response_handler.raise_ftp_error_for_values(response, [1, 3])
    ftp_response_handler.raise_ftp_failure_for_values(response, [4, 5])
    ftp_response_handler.raise_error_if_not_in_given_values(response, [2])