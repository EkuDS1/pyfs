class IOHandler:
    def __init__(self, conn):
        self.conn=conn
        self.outstr=""

    # Prints given prompt and requests input from client
    def input(self, prompt):
        # Print prompt to out stream
        self.output(prompt,"")
        self.flush()
        
        # Request client for input
        self.conn.sendall('i'.encode('utf-8'))
        # Return next line in input stream from client
        return self.conn.recv(1024).decode('utf-8')

    # Concatenates given string to outstr which can be sent to the client with flush()
    def output(self,output_string,endChar='\n'):
        self.outstr += output_string + endChar
    
    # Informs the client that output is being sent and then sends entire output string outstr
    def flush(self):
        # Request client to prepare for output
        self.conn.sendall('o'.encode('utf-8'))
        # Send client the output in a 1024 byte packet
        self.conn.sendall(self.outstr.ljust(1024, '\0').encode('utf-8'))
        self.outstr=""

    # Informs the client that the server is closing the connection
    def close(self):
        # Request client to close the connection
        self.conn.sendall('e'.encode('utf-8'))
