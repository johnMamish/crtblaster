import socket
import time

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(("localhost", 14484))
    time.sleep(0.1)
    print(sock.recv(1024))
    #print(sock.recv(1024))
    sock.sendall(f"is_playing\r\n".encode("utf-8"))
    sock.sendall(f"f off\r\n".encode("utf-8"))
    print(sock.recv(1024))




