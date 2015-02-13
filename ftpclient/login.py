import ftp_response_handler
import response


USER_COMMAND = "USER anonymous\r\n"
PASSWORD_COMMAND = 'PASS anonymous@gustavus.edu\r\n'
ACCOUNT_COMMAND = 'ACCT anonymous\r\n'


def user_login_process(socket_file):
    user_response_code = user_entry(socket_file)
    if user_response_code == 3:
        pass_response_code = password_entry(socket_file)
        if pass_response_code == 3:
            acct_entry()


def user_entry(socket_file):
    socket_file.write(USER_COMMAND)
    socket_file.flush()
    response_x = response.get_response(socket_file)
    ftp_response_handler.validate_user_and_pass_response(response_x)
    return int(response_x[0:1])


def password_entry(socket_file):
    socket_file.write(PASSWORD_COMMAND)
    socket_file.flush()
    pass_response = response.get_response(socket_file)
    ftp_response_handler.validate_user_and_pass_response(pass_response)
    return int(pass_response[0:1])


def acct_entry(socket_file):
    socket_file.write(ACCOUNT_COMMAND)
    socket_file.flush()
    acct_response = response.get_response(socket_file)
    ftp_response_handler.validate_acct_response(acct_response)