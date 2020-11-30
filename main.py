# pickle is used to store objects
from FileSystem import FileSystem
import pickle
import os.path

class File:
    def __init__(self, name):
        self.name = name
        self.chunks = fs.allocateFile()
        self.length = 0

    def write(self, input):
        chunksAndLength = fs.Write_to_File(self.chunks, self.length, input)
        self.chunks = chunksAndLength[0]
        self.length = chunksAndLength[1]
    def read(self):
        return fs.Read_from_File(self.chunks)

class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.childdir = {}
        self.childfiles = {}
    
    # Create directory
    def mkdir(self, dirname):
        if dirname in self.childdir:
            print("Folder already exists!")
        else:
            self.childdir[dirname] = Directory(dirname, self)
    
    # Delete directory
    def rmdir(self, dirname):
        if dirname in self.childdir:
            del self.childdir[dirname]
        else:
            print("No such folder found to delete")
    
    # Create file
    def mkfile(self, filename):
        if filename in self.childfiles:
            print("File already exists!")
        else:
            self.childfiles[filename] = File(filename)
        
    
    # Delete file
    def rmfile(self, filename):
        if filename in self.childfiles:
            del self.childfiles[filename]
        else:
            print("No such file found to delete")

    # set mode bits and return File object
    def open(self, filename, mode):
        self.childfiles[filename].mode = mode
        return self.childfiles[filename]
    
    # clear mode bits
    def close(self, filename):
        self.childfiles[filename].mode = ''

    # Recursively constructs the path of the folder we are in using a string
    def getPath(self):
        pathString = ''
        if self.parent != None:
            pathString += self.parent.getPath()
            pathString += '/' + self.name
        else:
            pathString += self.name
        
        return pathString
    
    # Displays folders and files, MS DOS(or Windows CMD) style
    def ls(self):
        if self.childdir:
            for dirname in self.childdir.keys():
                print(f'\t<DIR>\t{dirname}')
        if self.childfiles:
            for filename in self.childfiles.keys():
                print(f'\t\t{filename}\t')
        if not self.childdir and not self.childfiles:
            print("Empty Folder")
    
    def read(self,fileName):
      if fileName in self.childfiles:
        file=self.childfiles[fileName]
        print(file.read())
      else:
        print("File Not Found!")
        
    def write(self,fileName):
      
      if fileName in self.childfiles:
        file=self.childfiles[fileName]
        textBytes=input("Enter Data:")
        textBytes=textBytes.encode("utf-8")
        file.write(textBytes)
      else:
        print("File Not Found!")


# Stores updated directory data and closes program
def end_program(currentDir):
    
    # go to root
    while currentDir.parent != None:
        currentDir = currentDir.parent

    # store directory data as a binary file
    with open('fs.data', 'wb') as fileOut:
        pickle.dump(currentDir, fileOut)

    print("\n************ Program Closed ************")
    exit(0) # exit status 0 indicating that program closed without problems
    

################################## Main Code starts from here ##################################

if __name__ == "__main__":

    # If hard drive exists, load it as a stream and load the directory data
    if os.path.isfile('fs.data'):
        with open('fs.data', 'rb') as fileIn:
            currentDir = pickle.load(fileIn)
    # Otherwise, create hard drive and root folder with parent set to None
    else:
        with open("fs.data","wb") as out:
            out.truncate(1024*10)
            currentDir = Directory('root', None)
   
    fs = FileSystem(open('fs.data', 'r+b'))

    # Dictionary containing directory commands and their corresponding methods
    commandDic = {
        'mkdir' :  Directory.mkdir,
        'rmdir' :  Directory.rmdir,
        'mkfile' : Directory.mkfile,
        'rmfile' : Directory.rmfile,
        'read'  :  Directory.read,
        'write':   Directory.write
    }

    print('''
        ls to display available folders
        mkdir [dirname] to create folder
        rmdir [dirname] to remove a folder
        mkfile [filename] to create a file
        rmfile [filename] to remove a file

        read [filename] to read from a file
        write [filename] to write to a file

        cd [dirname] to enter the folder
        Also, 'cd ..' returns to previous folder
        exit to EXIT
        ''')

    while True:  
        # Prints the current path and gets input
        args = input(currentDir.getPath() + ': ')

        if args == 'exit':
            end_program(currentDir)
        elif args == 'ls':
            currentDir.ls()
        else:
            # When the input is a command with arguments, we split it
            # Here, args[0] is the command itself while args[1] should be its string argument 
            args = args.split(' ', 1)
            if args[0] == 'cd':
                if args[1] == '..':
                    currentDir = currentDir.parent
                elif args[1] in currentDir.childdir:
                    currentDir = currentDir.childdir[args[1]]
                else: print("Folder not found.")
            elif args[0] in commandDic:
                commandDic[args[0]](currentDir, args[1])
            else:
                print("ERROR: No such command found!")