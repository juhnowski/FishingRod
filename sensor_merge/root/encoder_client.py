#call python test_client.py file_name_or_stop_command_without_spaces
import socket
import sys

def client(string):
    HOST, PORT = 'localhost', 9002
    # SOCK_STREAM == a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.setblocking(0)  # optional non-blocking
    sock.connect((HOST, PORT))
    sock.send(string)
    reply = sock.recv(16384)  # limit reply to 16K
    sock.close()
    return reply
 
client(str(sys.argv[1]))    
