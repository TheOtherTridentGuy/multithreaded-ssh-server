# Copyright (c) 2024 Aiden Bohlander aka TheTridentGuy
# Released under GPL v3.0: https://www.gnu.org/licenses/gpl-3.0

import paramiko
import socket  
import threading  

class SSHInterface:
    def __init__(self, ip, port, callback) -> None: 
        self.ip = ip
        self.port = port
        self.callback = callback
    
    def start(self):
        self.host_key = paramiko.RSAKey.generate(2048)
        self.server = self.Server()
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.ip, self.port))
        sock.listen(100)
        print("[*] Socket listening")
        while True:
            conn, addr = sock.accept()
            print(f"[*] Connection from {addr[0]}:{addr[1]}, starting handler...")
            handler = threading.Thread(target=self.handle, args=(conn, addr))
            handler.start()
            print("[*] Started handler...")
    
    class Server(paramiko.server.ServerInterface): 
        def get_allowed_auths(self, username): 
            return "none"
        
        def check_channel_request(self, kind, channelID):
            return paramiko.OPEN_SUCCEEDED
        
        def check_channel_shell_request(self, channel):
            return True
        
        def check_channel_pty_request(self, c, t, w, h, p, ph, m):
            return True
        
        def get_banner(self):
            return ("Paramiko SSH Server v1.0 - NoneAuth version\n\r", "EN")

        def check_auth_none(self, username):
            print(f"[*] NoneAuth request with username {username}")
            return paramiko.AUTH_SUCCESSFUL

    def handle(self, conn, addr):
        print("[*] Handler waiting for SSH connection...")
        transport = paramiko.Transport(conn)
        transport.add_server_key(self.host_key)
        transport.start_server(server=self.server)
        channel = transport.accept(30) 
        if channel:
            print("[*] SSH connection recieved")
            self.callback(channel)
            channel.close()


def example_callback(channel):
    channel.send("Hi :)\r\n")
    while True:
        while not channel.recv_ready():
            pass
        data = channel.recv(1024)
        print(f"[>] {data}")
        channel.sendall(data)

if __name__ == "__main__":
    intf = SSHInterface("localhost", 5555, example_callback)
    intf.start()
