class IOHandler:
    def __init__(self, inputfile, outputfile):
        self.istream = open(inputfile,'r')
        self.ostream = open(outputfile,"w")
        
    def input(self, prompt):
        # Print prompt to out stream
        print(prompt, file=self.ostream)

        # Return next line in input stream
        return self.istream.readline()

    def __del__(self):
        self.istream.close()
        self.ostream.close()