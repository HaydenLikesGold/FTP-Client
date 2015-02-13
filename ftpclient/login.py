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
    user_response = response.get_response(socket_file, USER_COMMAND)
    ftp_response_handler.validate_user_and_pass_response(user_response)
    return int(user_response[0:1])


def password_entry(socket_file):
    pass_response = response.get_response(socket_file, PASSWORD_COMMAND)
    ftp_response_handler.validate_user_and_pass_response(pass_response)
    return int(pass_response[0:1])


def acct_entry(socket_file):
    acct_response = response.get_response(socket_file, ACCOUNT_COMMAND)
    ftp_response_handler.validate_acct_response(acct_response)