import socket

class Client:
    def __init__(self, hostIP):
        self.host=hostIP
        self.port=95
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)    
        self.client.connect((self.host,self.port))
    
    # Program consists of a loop waiting for signals from the server
    # Signals are 1 byte characters that indicate what the client should do
    # 'i' means input, 'o' means output, 'e' means exit program
    def program(self):
        while True:
            request = self.client.recv(1).decode("utf-8")
            # i for input
            if request == 'i':
                inp = input("")
                self.client.send(inp.encode("utf-8"))
            # o for output
            elif request == 'o':
                text=""
                text=self.client.recv(1024).decode("utf-8")
                text = text.rstrip("\x00")
                print(text,end="")
            # e for exit
            elif request == 'e':
                self.closeClient()
                break

    def closeClient(self):
            self.client.close()



if __name__=="__main__":
    hostIP = input("What ip do you wish to connect to?: ")
    c=Client(hostIP)
    c.program()

