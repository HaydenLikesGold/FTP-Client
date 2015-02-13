"""Manages errors from a given response and a list of values"""


def raise_ftp_error_for_values(response, list_of_values):
    """ftp errors passed in based on RFC"""
    response_value = int(response[0:1])
    for return_code in list_of_values:
        if response_value == return_code:
            raise RuntimeError("FTP error: " + response)


def raise_ftp_failure_for_values(response, list_of_values):
    """ftp failures passed in based on RFC"""
    response_value = int(response[0:1])
    for return_code in list_of_values:
        if response_value == return_code:
            raise RuntimeError("FTP failure: " + response)


def raise_error_if_not_in_given_values(response, list_of_values):
    """Expected values passed in based on RFC"""
    response_value = int(response[0:1])
    for return_code in list_of_values:
        if response_value == return_code:
            return
    raise RuntimeError("Unexpected FTP response: " + response)


def validate_pasv_and_quit_command(response):
    raise_ftp_error_for_values(response, [1, 3])
    raise_ftp_failure_for_values(response, [4, 5])
    raise_error_if_not_in_given_values(response, [2])


def validate_user_and_pass_response(response):
    raise_ftp_error_for_values(response, [1])
    raise_ftp_failure_for_values(response, [4, 5])
    raise_error_if_not_in_given_values(response, [2, 3])


def validate_retr_command(response):
    raise_ftp_error_for_values(response, [3])
    raise_ftp_failure_for_values(response, [4, 5])
    raise_error_if_not_in_given_values(response, [1, 2])


def validate_acct_response(response):
    raise_ftp_error_for_values(response, [1, 3])
    raise_ftp_failure_for_values(response, [4, 5])
    raise_error_if_not_in_given_values(response, [2])