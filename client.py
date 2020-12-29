import socket

class Client:
    def __init__(self):
        self.host='localhost'
        self.port=95
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect((self.host,self.port))
    def program(self):
        inp=input("Send to server: ")
        while inp.lower().strip()!="exit":
            self.client.send(inp.encode("utf-8"))
            text=self.client.recv(1024).decode("utf-8")
            print("Message received from Server: ",text)
            inp=input("Send to Server: ")
        self.closeClient()
    def closeClient(self):
            self.client.close()



if __name__=="__main__":
    c=Client()
    c.program()
