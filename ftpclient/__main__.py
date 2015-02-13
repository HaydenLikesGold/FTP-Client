import sys
from file_transfer import FileTransfer

def run_transfer():
    if len(sys.argv) == 1:
        server_name = 'ftp.cs.princeton.edu'
        server_port = 21
        file_path = '/pub/cs126/nbody/3body.txt'
    else:
        server_name = str(sys.argv[1])
        server_port = int(sys.argv[2])
        file_path = str(sys.argv[3])

    x = FileTransfer(server_name, server_port, file_path)
    x.ftp_process()

if __name__ == "__main__":
    run_transfer()