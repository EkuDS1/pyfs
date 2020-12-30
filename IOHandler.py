class IOHandler:
    def __init__(self, conn):
        self.conn=conn
        self.outstr=""

    def input(self, prompt):
        # Print prompt to out stream
        self.outstr+=prompt
        # Return next line in input stream
        return self.conn.recv(1024).decode('utf-8')

    def output(self,output_string,endChar='\n'):
        self.outstr+=output_string+endChar
    
    def flush(self):
        self.conn.sendall(self.outstr.encode('utf-8'))
        self.outstr=""

