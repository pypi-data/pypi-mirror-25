from pycube90 import Cube
import socket
import os

# v0.2.2

class CubeSocket:
    def __init__(self, key, protocol="TCP", dc=1):
        self.key = key
        self.session_key = key
        self.key_length = 16
        self.nonce_length = 8
        self.direct_connect = dc
        if protocol == "TCP":
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif protocol == "UDP":
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def wrap(self, sock):
        self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def close(self):
        self.sock.close()

    def listen(self, num_listeners):
        self.sock.listen(num_listeners)

    def bind(self, host, port):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))

    def cli_keyexchange(self, sock):
        nonce = self.gen_key(self.nonce_length)
	self.session_key = self.gen_key(self.key_length)
        key = Cube(self.key, nonce).encrypt(self.session_key)
    	self.sock.send(nonce+key)

    def srv_keyexchange(self, client_sock):
        buf = client_sock.recv(self.nonce_length+self.key_length)
        nonce = buf[0:self.nonce_length]
        key = buf[self.nonce_length:]
        self.session_key = Cube(self.key, nonce).decrypt(key)

    def accept(self):
        client, addr = self.sock.accept()
        if self.direct_connect == 0:
	    self.srv_keyexchange(client)
        return client, addr

    def gen_key(self, length):
        key = ""
        for x in range(0,length):
            char = chr((ord(os.urandom(1)) % (122 - 32 + 1)) + 32)
            key += char
        return key

    def cubeconnect(self, host, port):
        self.connect(host, port)
	self.cli_keyexchange(self.sock)

    def send(self, buf):
        nonce = self.gen_key(self.nonce_length)
        if self.direct_connect == 1:
            buf = Cube(self.key, nonce).encrypt(buf)
        else:
            buf = Cube(self.session_key, nonce).encrypt(buf)
        self.sock.send(nonce+buf)

    def recv(self, buf_size):
        buf = self.sock.recv(self.nonce_length+buf_size)
        nonce = buf[0:self.nonce_length]
        payload = buf[self.nonce_length:]
        if self.direct_connect == 1:
            content = Cube(self.key, nonce).decrypt(payload)
        else:
            content = Cube(self.session_key, nonce).decrypt(payload)
        return content

    def sendto(self, buf, ip, port):
        nonce = self.gen_key(self.nonce_length)
        buf = Cube(self.key, nonce).encrypt(buf)
        self.sock.sendto(nonce+buf, (ip, port))

    def recvfrom(self, buf_size):
        buf, addr = self.sock.recvfrom(buf_size)
        nonce = buf[0:self.nonce_length]
        data = buf[self.nonce_length:]
        data = Cube(self.key, nonce).decrypt(data)
        return data

class CubeWrap:
    def __init__(self, sock, key, protocol="TCP", dc=1):
        self.cubesock = CubeSocket(key, protocol, dc)
        self.cubesock.wrap(sock)
        self.raw_sock = sock
