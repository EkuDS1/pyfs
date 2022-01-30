import socket
from _thread import *

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
        
    def process(self,conn,run,currDir):
        run(currDir,conn)
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        print("Connection closed")

    def acceptConn(self,run,currDir):
        while True:
            conn,addr=self.sock.accept()#Accept any incoming connection
            print("New connection accepted: ",conn,addr)
            start_new_thread(self.process,(conn,run,currDir))#Create new thread with process and connection object
