# pickle is used to store objects
from FileSystem import FileSystem
import pickle
import os.path
from bitarray import bitarray
chunk_size=256
size=1024*10



class File:
    def __init__(self, name):
        self.name = name
        self.chunks = fs.allocateFile()
        self.length = 0

    def deleteFile(self):
        fs.deallocateFile(self.chunks)

    def write(self, input):
        chunksAndLength = fs.Write_to_File(self.chunks, self.length, input)
        self.chunks = chunksAndLength[0]
        self.length = chunksAndLength[1]

    def read(self):
        return fs.Read_from_File(self.chunks)

    def move(self,from_,to,size):
        s=len(self.chunks)*chunk_size
        sA=self.chunks[0]*chunk_size
        from_=int(from_)
        to=int(to)
        size=int(size)
        if from_ >= 0 and from_ < s and to >= 0 and to+s < s and size < s and size >= 0:
            from_=sA+from_
            to=sA+to
            fs.move_within_file(from_,to,size)
        else:
            print("Out Of File Index!")

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
            if not self.childdir[dirname].childfiles:
                del self.childdir[dirname]
            else:
                print("This folder contains files!")
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
            self.childfiles[filename].deleteFile()
            del self.childfiles[filename]
        else:
            print("No such file found to delete")

    # Move file to another folder
    def mvfile(self, filename, path):
        if filename in self.childfiles:
            newDir = cd(self, path.split('/'))
            if newDir == self:
                print("Error: Move operation failed!")
                return
            newDir.childfiles[filename] = self.childfiles[filename]
            del self.childfiles[filename]
        else:
            print("No such file found to move")
            return

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

    def move_file(self,fileName,from_,to,size):
        if fileName in self.childfiles:
            file=self.childfiles[fileName]
            file.move(from_,to,size)
        else:
            print("File Not Found!")

# returns Directory object based on the current directory and the given path
def cd(currentDirInput, pathArr):

    if not pathArr or pathArr[0] == '':
        return currentDirInput

    tempDir = currentDirInput 

    # Create dictionary containing Directory objects for root folder and child folders
    tempDirDict = {
        'root' : root,
    }
    tempDirDict.update(tempDir.childdir)

    if pathArr[0] in tempDirDict:
        tempDir = cd(tempDirDict[pathArr[0]], pathArr[1:])
    elif pathArr[0] == '..':
        if tempDir.parent != None:
            tempDir = cd(tempDir.parent, pathArr[1:])
        else:
            tempDir = currentDir
            print("Root has no parent folder.")
    else:
        tempDir = currentDir
        print("Folder not found.")
    
    return tempDir

# Stores updated directory data and closes program
def end_program():
    # go to root
    currentDir = root

    # store directory data as a binary file
    with open('fs.data', 'r+b') as fileOut:
        pickle.dump((currentDir,fs.getBitArray()), fileOut,pickle.HIGHEST_PROTOCOL)
        
    print("\n************ Program Closed ************")
    exit(0) # exit status 0 indicating that program closed without problems
    

################################## Main Code starts from here ##################################

if __name__ == "__main__":
    
    # If hard drive exists, load it as a stream and load the directory data
    if os.path.isfile('fs.data'):
        with open('fs.data', 'r+b') as fileIn:
            dirAndBitArray= pickle.load(fileIn)
            currentDir = dirAndBitArray[0]
            bitArray = dirAndBitArray[1]
            print(bitArray)
    # Otherwise, create hard drive and root folder with parent set to None
    else:
        with open("fs.data","wb") as out:
            out.truncate(1024*10)
            bitArray=bitarray(int(size/chunk_size))
            bitArray.setall(0)
            bitArray[0:4]=True
            
            currentDir = Directory('root', None)
    fs = FileSystem(open('fs.data', 'r+b'))
    fs.setBitArray(bitArray)

    root = currentDir   # Used for changing directories

   # Dictionary containing directory commands and their corresponding methods
    commandDic = {
        'mkdir'  : Directory.mkdir,
        'rmdir'  : Directory.rmdir,
        'mkfile' : Directory.mkfile,
        'rmfile' : Directory.rmfile,
        'mvfile' : Directory.mvfile,
        'read'   : Directory.read,
        'write'  : Directory.write,
        'move'   : Directory.move_file,
        'ls'     : Directory.ls
    }

    print('''
        ls to display available folders
        mkdir [dirname] to create folder
        rmdir [dirname] to remove a folder
        mkfile [filename] to create a file
        rmfile [filename] to remove a file

        read [filename] to read from a file
        write [filename] to write to a file

        move [filename] [from] [to] [size] to move text within the file

        cd [dirname] to enter the folder
        Also, 'cd ..' returns to previous folder
        exit to EXIT
        ''')

    while True:  
        # Prints the current path and gets input
        # To get arguments to the commands, we split the input into a maximum of 5 parts
        args = input(currentDir.getPath() + ': ').split(' ', 5)

        # Here, args[0] is the command itself while args[1] onwards should be its string argument 
        if args[0] == 'exit':
            end_program()

        elif args[0] == 'cd':
            currentDir = cd(currentDir, args[1].split('/'))

        elif args[0] in commandDic:
            if len(args) == 1:
                commandDic[args[0]](currentDir)
            elif len(args) == 2:
                commandDic[args[0]](currentDir, args[1])
            elif len(args) == 3:
                commandDic[args[0]](currentDir, args[1], args[2])
            elif len(args) == 5:
                commandDic[args[0]](currentDir, args[1], args[2], args[3], args[4])
            else: print("Argument Error!")
        else:
            print("ERROR: No such command found!")
            
            