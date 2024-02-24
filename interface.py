import paramiko
import socket  
import threading  

class Server(paramiko.server.ServerInterface): 
    def get_allowed_auths(self, username): 
        return "password"
    
    def check_channel_request(self, kind, channelID):
        return paramiko.OPEN_SUCCEEDED
    
    def check_channel_shell_request(self, channel):
        return True
    
    def check_channel_pty_request(self, c, t, w, h, p, ph, m):
        return True
    
    def get_banner(self):
        return ("Paramiko SSH Server v1.0\n\r", "EN")

    def check_auth_password(self, username, password):
        print(f"[*] Auth request with credentials {username}:{password}")
        return paramiko.AUTH_SUCCESSFUL

def handle(conn, addr):
    print("[*] Handler waiting for SSH connection...")
    transport = paramiko.Transport(conn)
    transport.add_server_key(host_key)
    transport.start_server(server=server)
    channel = transport.accept(30) 
    if channel:
        print("[*] SSH connection recieved")
        channel.send("Hi :)\r\n")
        print(f"[>] {channel.recv(1024)}")
        channel.close()


host_key = paramiko.RSAKey.generate(2048)
server = Server()
sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("127.0.0.1", 5555))
sock.listen(100)
print("[*] Socket listening")
while True:
    conn, addr = sock.accept()
    print(f"[*] Connection from {addr[0]}:{addr[1]}, starting handler...")
    handler = threading.Thread(target=handle, args=(conn, addr))
    handler.start()
    print("[*] Started handler...")
    