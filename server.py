import socket
import threading
from _thread import *
import time

class Server:
    def __init__(self):
        self.host='localhost'#Loop back host
        self.port=95#Port
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#Create a socket object with tcp protocol
        try:
            self.sock.bind((self.host,self.port))#Binding to host and port
        except socket.error as e:
            print(str(e))
        self.sock.listen(2)
        print("Server is ready!")
        print("Waiting for connection")
        

    def process(self,conn):
        while True:
            data=conn.recv(1024)#Recieves max 1024 bytes packet from client  
            if not data:
                break
            print(data)
            #modifies data
            data=data.decode('utf-8')+"123"
            data=data.encode('utf-8')
            conn.sendall(data)
            
        conn.close()
    def acceptConn(self):
        while True:
            conn,addr=self.sock.accept()#Accept any incoming connection
            print("New connection accepted: ",conn,addr)
            start_new_thread(self.process,(conn,))#Create new thread with process and connection object
if __name__=="__main__":
    s=Server()
    s.acceptConn() 
