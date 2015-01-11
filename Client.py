from socket import *

#General Helpers
def response_to_port_tuple(response):
	hostAddress = response[response.find('(')+1:]
	hostAddress = hostAddress.replace(')', '')
	arrayOfInfo = hostAddress.split(',')

	hostName = arrayOfInfo[0]+'.'+arrayOfInfo[1]+'.'+arrayOfInfo[2]+'.'+arrayOfInfo[3]
	portNumber = ((int(arrayOfInfo[4]))*256) + int(arrayOfInfo[5])

	return (hostName, portNumber)

def get_response():
	while True:
		line = _socketFile.readline()
		if (line[0].isdigit() and line[1].isdigit and line[2].isdigit and line[3] == " "):
			return line

def get_retr_response():
	string_buffer = ''
	while True:
		new_line = _createdFile.readline()
		if not new_line: return string_buffer
		string_buffer += new_line

#Error Helpers
def raise_errors_for_values(response, list_of_values):
	response_value = int(response[0:1])
	for return_code in list_of_values:
		if response_value == return_code:
			raise RuntimeError("FTP error: " + response)

def raise_failures_for_values(response, list_of_values):
	response_value = int(response[0:1])
	for return_code in list_of_values:
		if response_value == return_code:
			raise RuntimeError("FTP failure: " + response)

def raise_alert_if_value_isnt(response, list_of_values):
	response_value = int(response[0:1])
	for return_code in list_of_values:
		if response_value == return_code:
			return
	raise RuntimeError("Unexpected FTP response: " + response)

#Login Process
def user_login_process():
	user_response_code = user_entry()
	if (user_response_code == 3):
		pass_response_code = password_entry()
		if (pass_response_code == 3):
			acct_entry()

def user_entry():
	_socketFile.write("USER anonymous\r\n")
	_socketFile.flush()
	response = get_response()
	validate_user_and_pass_response(response)
	return int(response[0:1])

def password_entry():
	_socketFile.write('PASS anonymous@gustavus.edu\r\n')
	_socketFile.flush()
	pass_response = get_response()
	validate_user_and_pass_response(pass_response)
	return int(pass_response[0:1])

def validate_user_and_pass_response(response):
	raise_errors_for_values(response, [1])
	raise_failures_for_values(response, [4,5])
	raise_alert_if_value_isnt(response, [2,3])

def acct_entry():
	_socketFile.write('ACCT anonymous\r\n')
	_socketFile.flush()
	acct_response = get_response()
	validate_acct_response(acct_response)

def validate_acct_response(response):
	raise_errors_for_values(response, [1,3])
	raise_failures_for_values(response, [4,5])
	raise_alert_if_value_isnt(response, [2])

#Connection Process
def connect_to_princeton_server():
	serverName = 'ftp.cs.princeton.edu'
	serverPort = 21
	_clientSocket.connect((serverName, serverPort))
	_clientSocket.close()
	get_response()

def connect_to_new_socket():
	pasv_port = send_pasv_command()
	_createdSocket.connect(pasv_port)
	_createdSocket.close()

def send_pasv_command():
	_socketFile.write('PASV\r\n')
	_socketFile.flush()
	newPortInformation = get_response()
	validate_pasv_and_quit_command(newPortInformation)
	return response_to_port_tuple(newPortInformation)

def validate_pasv_and_quit_command(response):
	raise_errors_for_values(response, [1,3])
	raise_failures_for_values(response, [4,5])
	raise_alert_if_value_isnt(response, [2])

def send_retr_command():
	_socketFile.write('RETR /pub/cs126/nbody/3body.txt\r\n')
	_socketFile.flush()
	validate_retr_command(get_response())
	validate_retr_command(get_response())

def validate_retr_command(response):
	raise_errors_for_values(response, [3])
	raise_failures_for_values(response, [4,5])
	raise_alert_if_value_isnt(response, [1,2])

def retrieve_data():
	send_retr_command()
	return get_retr_response()

def close_server_connection():
	_socketFile.write('QUIT\r\n')
	_socketFile.flush()
	validate_pasv_and_quit_command(get_response())

def get_server_response_less_basic():
	global _clientSocket
	global _createdSocket
	global _socketFile
	global _createdFile

	_clientSocket = socket(SOCK_DGRAM)
	_createdSocket = socket(SOCK_DGRAM)
	_socketFile = _clientSocket.makefile(mode = "rw")
	_createdFile = _createdSocket.makefile(mode = "rw")

	connect_to_princeton_server()
	user_login_process()
	connect_to_new_socket()
	data = retrieve_data()

	close_server_connection()
	return data

print(get_server_response_less_basic())
