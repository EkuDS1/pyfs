# pickle is used to store objects
from FileSystem import FileSystem
import pickle
import os.path
from bitarray import bitarray
import sys
import threading

chunk_size=256
size=1024*10
dirChunks = 4

class File:
    def __init__(self, name, fileChunks):
        self.name = name
        self.chunks = fileChunks
        self.length = 0

    def deleteFile(self):
        fs.deallocateFile(self.chunks)
    
    def write_at(self, at):
            at=int(at)
            if at>=0 and at<len(self.chunks)*chunk_size:
                input_ = input('Enter Data: ')
                input_=input_.encode("utf-8")
                chunksAndLength=fs.write_at(self.chunks,self.length,input_,at)
                self.chunks = chunksAndLength[0]
                self.length = chunksAndLength[1]
            else:
                print("Please enter a location inside the file!")
            
            
    def write(self):
            input_ = input('Enter Data: ')
            input_=input_.encode("utf-8")
            
            chunksAndLength = fs.Write_to_File(self.chunks, self.length, input_)
            self.chunks = chunksAndLength[0]
            self.length = chunksAndLength[1]
            
    def read(self):
        print(fs.Read_from_File(self.chunks))

    def read_at(self, at, readSize):
        at = int(at)
        readSize = int(readSize)
        if (at + readSize) <= self.length and at >=0 and readSize >=0:
            print(fs.read_at(self.chunks,at, readSize))
        else:
            print("Error: Trying to read outside of file!")

    def move_in(self, fromAddr, toAddr, selectionSize):

        fromAddr = int(fromAddr)
        toAddr = int(toAddr)
        selectionSize = int(selectionSize)
        
        total_size=len(self.chunks)*chunk_size

        
        if fromAddr >= 0 and fromAddr < total_size and toAddr >= 0 and toAddr < total_size and selectionSize < total_size and selectionSize >= 0:
            self.length = fs.move_within_file(fromAddr,toAddr,selectionSize,self.chunks,self.length)
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
            
            if dirTooBig():
                print("Error! Directory table too large. Cannot create directory.")
                self.rmdir(dirname)
                return
    
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
            try:
                fileChunks = fs.allocateFile()
            except (IndexError):
                print("Error! No more space on disk. Please delete a file.")
                return
            self.childfiles[filename] = File(filename, fileChunks)
            
            # Compress and serialize entire directory tree and check if it's too big to fit in the given chunks
            bytesToStore = pickle.dumps((root, fs.getBitArray()),pickle.HIGHEST_PROTOCOL)

            if dirTooBig():
                print("Error! Directory table too large. Cannot create file.")
                self.rmfile(filename)
                return
        
    
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
    def open_(self, filename):
        flag=0
        if filename in self.childfiles:
            file=self.childfiles[filename]
            fileDic={
                'read'      :  file.read,
                'write'     :  file.write,
                'move'      :  file.move_in,
                'write_at'  :  file.write_at,
                'read_at'   :  file.read_at
            }
            print('''
                Choose an operation to perform on the file: 
                    read
                    write
                    write_at [address in file]
                    read_at [address in file] [size]
                    move [from address] [to address] [size]
                ''')
            while flag!=1:
                fileargs=input("Operation: ").split()

                # Do nothing if empty input is entered
                if fileargs == []:
                    continue
                if fileargs[0]=="close" and len(fileargs) == 1:
                    flag=self.close(filename)
                elif fileargs[0] in fileDic:
                    try:
                        if len(fileargs) == 1:
                            fileDic[fileargs[0]]()
                        elif len(fileargs) == 2:
                            fileDic[fileargs[0]](fileargs[1])
                        elif len(fileargs) == 3:
                            fileDic[fileargs[0]](fileargs[1], fileargs[2])
                        elif len(fileargs) == 4:
                            fileDic[fileargs[0]](fileargs[1], fileargs[2], fileargs[3])
                        else:
                            print("Error: Please enter correct arguments.")
                    except TypeError as e:
                        print("TypeError:",e.args)
                        print("Error: Please enter correct arguments.")
                        
                else:
                    print("Invalid Command!")
            
            
        else:
            print("File Not Found!")
        
    # clear mode bits
    def close(self, filename):
        return 1

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
    
    def memorymap(self, prefix=""):
        if prefix=="":
            print(self.name)
            prefix = "|  "
        for file in self.childfiles:
            print(prefix+"<file>",self.childfiles[file].name, str( [element * 256 for element in self.childfiles[file].chunks ]))
        for directory in self.childdir:
            print(prefix+"<dir>", self.childdir[directory].name)
            self.childdir[directory].memorymap(prefix+"|  ")

# Utility function which checks if the directory structure is too big to be stored on the given chunks
def dirTooBig():
    bytesToStore = pickle.dumps((root, fs.getBitArray()),pickle.HIGHEST_PROTOCOL)
    if sys.getsizeof(bytesToStore) > (dirChunks * chunk_size):
        return True
    else: 
        return False

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


def run(currentDir,file):
    #Stdin should not be accessed by multiple threads
    #as it will cause file inputs to mix and cause crashes
    #so stdin will be locked by each thread when its used. 
    
    #stdin to take input from a file
    stdinLock.acquire()
    sys.stdin=open("stdin-scripts/"+file,'r')
    #stdout to output to a file
    sys.stdout=open("stdout-scripts/"+file,"w")
    
    while True:
        # Prints the current path and gets input
        # To get arguments to the commands, we split the input into a maximum of 5 parts
        args = input(currentDir.getPath() + ': ').split(' ', 5)
        # Do nothing if empty input is entered
        if args == ['']:
            continue
        # Here, args[0] is the command itself while args[1] onwards should be its string argument
        elif args[0] == 'exit' and len(args) == 1:
            end_program()
            stdinLock.release()
            break
        elif args[0] == 'cd' and len(args) == 2:
            currentDir = cd(currentDir, args[1].split('/'))
        elif args[0] in commandDic:
            try:
               if len(args) == 1:
                   commandDic[args[0]](currentDir)
               elif len(args) == 2:
                   commandDic[args[0]](currentDir, args[1])
               elif len(args) == 3:
                   commandDic[args[0]](currentDir, args[1], args[2])
               elif len(args) == 5:
                   commandDic[args[0]](currentDir, args[1], args[2], args[3], args[4])
               else: print("Argument Error!")
            except TypeError:
                print("Error: Please only enter required arguments.")  
        else:
            print("ERROR: No such command found!")
    
        
# Stores updated directory data and closes program
def end_program():
    # go to root
    currentDir = root
    
    # store directory data as a binary file
    with open('fs.data', 'r+b') as fileOut:
        pickle.dump((currentDir,fs.getBitArray()), fileOut,pickle.HIGHEST_PROTOCOL)
        
    print("\n************ Program Closed ************")
    
    

################################## Main Code starts from here ##################################

if __name__ == "__main__":
    
    # If hard drive exists, load it as a stream and load the directory data
    if os.path.isfile('fs.data'):
        with open('fs.data', 'r+b') as fileIn:
            # Loads tuple containing both Directory and bitarray objects
            dirAndBitArray= pickle.load(fileIn)
            currentDir = dirAndBitArray[0]
            bitArray = dirAndBitArray[1]
            
    # Otherwise, create hard drive and root folder with parent set to None
    else:
        with open("fs.data","wb") as out:
            out.truncate(size)
            bitArray=bitarray(int(size/chunk_size))
            bitArray.setall(0)
            bitArray[0:dirChunks]=True
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
        'open'   : Directory.open_,
        'ls'     : Directory.ls,
        'memmap' : Directory.memorymap
    }

    print('''
        ls to display available folders
        mkdir [dirname] to create folder
        rmdir [dirname] to remove a folder
        mkfile [filename] to create a file
        rmfile [filename] to remove a file
        mvfile [filename] [path] to move file to another folder
        cd [dirname] to enter the folder
        Also, 'cd ..' returns to previous folder

        memmap to view memory map of the filesystem

        exit to EXIT
        ''')
    #Create a shared lock
    stdinLock=threading.Lock()
    if(len(sys.argv)!=2):
        print("Please enter number of threads!")
        exit(0)
    thr=int(sys.argv[1])

    threads=list()
    for i in range(thr):
        thread=threading.Thread(target=run,args=(currentDir,f"script{i}.txt"))#Creating threads
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()#waiting for threads to finish