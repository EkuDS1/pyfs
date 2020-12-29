import socket
import threading
from _thread import *
import time

class Server:
    def __init__(self):
        self.host='localhost'
        self.port=95
        self.text=""
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.sock.bind((self.host,self.port))
        except socket.error as e:
            print(str(e))
        self.sock.listen(2)
        print("Server is ready!")
        print("Waiting for connection")
        self.connections=[]

    def process(self,conn):
        while True:
            data=conn.recv(1024)
            if not data:
                break
            print(data)
            data=data.decode('utf-8')+"123"
            data=data.encode('utf-8')
            conn.sendall(data)
            
        conn.close()
    def acceptConn(self):
        while True:
            conn,addr=self.sock.accept()
            self.connections+=[(conn,addr)]
            print("New connection accepted: ",conn,addr)
            start_new_thread(self.process,(conn,))
if __name__=="__main__":
    s=Server()
    s.acceptConn() 
