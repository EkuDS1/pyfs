# pickle is used to store objects

from FileSystem import FileSystem, threadLocal
from IOHandler import IOHandler
import pickle
import os.path
from bitarray import bitarray
import sys
import threading
from server import Server
mutex = threading.Lock()

chunk_size=256
size=1024*10
dirChunks = 4

class File:
    def __init__(self, name, fileChunks):
        self.name = name
        self.chunks = fileChunks
        self.length = 0
        self.inuse = 0

    def deleteFile(self):
        fs.deallocateFile(self.chunks)
    
    def write_at(self, at):
        at=int(at)
        if at>=0 and at<len(self.chunks)*chunk_size:
            input_ = threadLocal.ioh.input('Enter Data: ')
            #threadLocal.ioh.output(listToString(input_)  )
            input_=input_.encode("utf-8")
            mutex.acquire()
            chunksAndLength=fs.write_at(self.chunks,self.length,input_,at)
            self.chunks = chunksAndLength[0]
            self.length = chunksAndLength[1]
            mutex.release()
        else:
            threadLocal.ioh.output("Please enter a location inside the file!")
                        
    def write(self):
        threadLocal.ioh.output("Write:")  
        input_ = threadLocal.ioh.input('Enter Data: ')
        #threadLocal.ioh.output(input_  )   
        input_=input_.encode("utf-8")
        
        mutex.acquire()
        chunksAndLength = fs.Write_to_File(self.chunks, self.length, input_)
        self.chunks = chunksAndLength[0]
        self.length = chunksAndLength[1]
        mutex.release()
        threadLocal.ioh.output("Write completed!")
 
    def read(self):
        ### TODO:
        #### adding semaphore
        threadLocal.ioh.output(fs.Read_from_File(self.chunks))
        
    def read_at(self, at, readSize):
        at = int(at)
        readSize = int(readSize)
        if (at + readSize) <= self.length and at >=0 and readSize >=0:
            # TODO:
            ##### adding semophore
            threadLocal.ioh.output(fs.read_at(self.chunks,at, readSize))
        else:
            threadLocal.ioh.output("Error: Trying to read outside of file!")

    def move_in(self, fromAddr, toAddr, selectionSize):
        fromAddr = int(fromAddr)
        toAddr = int(toAddr)
        selectionSize = int(selectionSize)
        total_size=len(self.chunks)*chunk_size
        
        if fromAddr >= 0 and fromAddr < total_size and toAddr >= 0 and toAddr < total_size and selectionSize < total_size and selectionSize >= 0:
            mutex.acquire()
            self.length = fs.move_within_file(fromAddr,toAddr,selectionSize,self.chunks,self.length)
            mutex.release()
        else:
            threadLocal.ioh.output("Out Of File Index!")

class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.childdir = {}
        self.childfiles = {}
    
    # Create directory
    def mkdir(self, dirname):
        if dirname in self.childdir:
            threadLocal.ioh.output("Folder already exists!")
        else:
            self.childdir[dirname] = Directory(dirname, self)       
            if dirTooBig():
                threadLocal.ioh.output("Error! Directory table too large. Cannot create directory.")
                self.rmdir(dirname)
                return
    
    # Delete directory
    def rmdir(self, dirname):
        if dirname in self.childdir:
            if not self.childdir[dirname].childfiles:
                del self.childdir[dirname]
            else:
                threadLocal.ioh.output("This folder contains files!")
        else:
            threadLocal.ioh.output("No such folder found to delete")
    
    # Create file
    def mkfile(self, filename):
        if filename in self.childfiles:
            threadLocal.ioh.output("File already exists!")
        else:
            try:
                fileChunks = fs.allocateFile()
            except (IndexError):
                threadLocal.ioh.output("Error! No more space on disk. Please delete a file.")
                return
            self.childfiles[filename] = File(filename, fileChunks)
            # Compress and serialize entire directory tree and check if it's too big to fit in the given chunks
            bytesToStore = pickle.dumps((root, fs.getBitArray()),pickle.HIGHEST_PROTOCOL)

            if dirTooBig():
                threadLocal.ioh.output("Error! Directory table too large. Cannot create file.")
                self.rmfile(filename)
                return

    # Delete file
    def rmfile(self, filename):
        if filename in self.childfiles:
            if self.childfiles[filename].inuse == 0:
                self.childfiles[filename].deleteFile()
                del self.childfiles[filename]
            else:
                threadLocal.ioh.output("File open in another thread")
        else:
            threadLocal.ioh.output("No such file found to delete")

    # Move file to another folder
    def mvfile(self, filename, path):
        if self.childfiles[filename].inuse == 0:
            if filename in self.childfiles:
                newDir = cd(self, path.split('/'))
                if newDir == self:
                    threadLocal.ioh.output("Error: Move operation failed!")
                    return
                newDir.childfiles[filename] = self.childfiles[filename]
                del self.childfiles[filename]
            else:
                threadLocal.ioh.output("No such file found to move")
                return
        else:
            threadLocal.ioh.output("File open in another thread")

    # set mode bits and return File object
    def open_(self, filename):
        flag=0
        if filename in self.childfiles:
            file=self.childfiles[filename]
            self.childfiles[filename].inuse += 1
            fileDic={
                'read'      :  file.read,
                'write'     :  file.write,
                'move'      :  file.move_in,
                'write_at'  :  file.write_at,
                'read_at'   :  file.read_at
            }
            ### Commented this because dont want to print this in terminal while using threads ###

            threadLocal.ioh.output('''
              Choose an operation to perform on the file: 
                    read
                    write
                    write_at [address in file]
                    read_at [address in file] [size]
                    move [from address] [to address] [size]
                ''')
            while flag!=1:
                fileargs=threadLocal.ioh.input('Operation: ').split()
                #threadLocal.ioh.output(listToString(fileargs))

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
                            if fileargs[0] == 'write_at':
                                fileDic[fileargs[0]](fileargs[1])
                            else:
                                fileDic[fileargs[0]](fileargs[1])
                        elif len(fileargs) == 3:
                            fileDic[fileargs[0]](fileargs[1], fileargs[2])
                        elif len(fileargs) == 4:
                            fileDic[fileargs[0]](fileargs[1], fileargs[2], fileargs[3])
                        else:
                            threadLocal.ioh.output("Error: Please enter correct arguments.")
                    except TypeError as e:
                        threadLocal.ioh.output("TypeError:" + str(e.args))
                        threadLocal.ioh.output("Error: Please enter correct arguments.")
                else:
                    threadLocal.ioh.output("Invalid Command!")        
        else:
            threadLocal.ioh.output("File Not Found!")
        # Flush all output from open function
        threadLocal.ioh.flush()  
        
    # clear mode bits
    def close(self, filename):
        self.childfiles[filename].inuse -= 1
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
                threadLocal.ioh.output(f'\t<DIR>\t{dirname}')
        if self.childfiles:
            for filename in self.childfiles.keys():
                threadLocal.ioh.output(f'\t\t{filename}\t')
        if not self.childdir and not self.childfiles:
            threadLocal.ioh.output("Empty Folder")
        
    def memorymap(self, prefix=""):
        if prefix=="":
            threadLocal.ioh.output(self.name)
            prefix = "|  "
        for file in self.childfiles:
            threadLocal.ioh.output(prefix + "<file> " + self.childfiles[file].name + " " + str( [element * 256 for element in self.childfiles[file].chunks ]))
        for directory in self.childdir:
            threadLocal.ioh.output(prefix + "<dir> " + self.childdir[directory].name)
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
            threadLocal.ioh.output("Root has no parent folder.")
    else:
        tempDir = currentDir
        threadLocal.ioh.output("Folder not found.")
    
    return tempDir

def sign_process():
    option = threadLocal.ioh.input("Do you have a account [ y | n ]: ")
    if option.lower() == "n":
        threadLocal.ioh.output("---- SIGN UP ----")
        while True:
            user_name = threadLocal.ioh.input("Enter the user name: ")
            if user_name in user_data:
                threadLocal.ioh.output("User already exists")
            else:
                user_password = threadLocal.ioh.input("Enter password: ")
                user_data[user_name] = user_password
                # storing the user logged in
                threadLocal.active_user = user_name
                threadLocal.ioh.output("User Created\nUser Logged in\n")
                break
    elif option.lower() == "y":
        threadLocal.ioh.output("---- SIGN IN ----")
        while True:
            user_name = threadLocal.ioh.input("Enter user name: ")
            user_password = threadLocal.ioh.input("Enter password: ")
            if user_name in user_data and user_password == user_data[user_name]:
                threadLocal.ioh.output(user_name+" User logged in\n")
                # storing the user logged in
                threadLocal.active_user = user_name
                break
            else:
                threadLocal.ioh.output("\033[0;31mWrong user name or password\033[0;0m")
                option2 = threadLocal.ioh.input("Press r to Retry or b to go back:")
                if option2.lower() == "b":
                    sign_process()
                    break
    else:
        sign_process()

def run(currentDir,conn):
    #Stdin should not be accessed by multiple threads
    #as it will cause file inputs to mix and cause crashes
    #so stdin will be locked by each thread when its used. 

    ioh = getattr(threadLocal, 'ioh', None)
    #it stores the user 
    active_user = getattr(threadLocal, 'active_user', None)
    if ioh is None:
        threadLocal.ioh = IOHandler(conn)
    
    sign_process()
    threadLocal.ioh.output("\033\t[1mCOMMANDS:\033[0m\n\t\tmkdir [dirname] --> Create Directory\n\t\trmdir [dirname] --> Delete Directory\n" +
                           "\t\tmkfile [filename] --> Create File\n\t\trmfile [filename] --> Delete File\n" +
                           "\t\topen [filename] --> open file\n\t\tmemmap --> view directory Structure\n" +
                           "\t\tmvfile [filename] [path] --> To move file\n\t\tls --> Shows currect Directory Structure\n")

    while True:
        # Prints the current path and gets input
        # To get arguments to the commands, we split the input into a maximum of 5 parts
        args = threadLocal.ioh.input(currentDir.getPath() + ":").split(' ', 5)
        #threadLocal.ioh.output( listToString(args) )
        # Do nothing if empty input is entered
        if args == ['']:
            continue
        # Here, args[0] is the command itself while args[1] onwards should be its string argument
        elif args[0] == 'exit' and len(args) == 1:
            end_program()
            threadLocal.ioh.flush()
            threadLocal.ioh.close()
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
               else: threadLocal.ioh.output("Argument Error!")
            except TypeError:
                threadLocal.ioh.output("Error: Please only enter required arguments.")  
        else:
            threadLocal.ioh.output("ERROR: No such command found! " + args[0] )
        threadLocal.ioh.flush()

# Stores updated directory data and closes program
def end_program():
    # go to root
    currentDir = root
    
    # store directory data as a binary file
    with open('fs.data', 'r+b') as fileOut:
        pickle.dump((currentDir,fs.getBitArray(),user_data), fileOut,pickle.HIGHEST_PROTOCOL)
        
    threadLocal.ioh.output("\n************ Program Closed ************")
    
def listToString(s):  
    str1 = ""  
    for ele in s:  
        str1 += ele + " "   
    return str1  
    
################################## Main Code starts from here ##################################

if __name__ == "__main__":
    
    # if(len(sys.argv)!=2):
    #     print ('''\033[93m\033[1m 
    #              Please enter number of threads! Run the code as
    #              " python  [python file name] [No. of threads] \" \033[0;0m\n''')
    #     exit(0)

    # try:
    #     thr=int(sys.argv[1])
    # except: 
    #     print ('''\033[93m\033[1m 
    #             Please enter the correct command! Run the code as
    #              " python [python file name] [No. of threads] \" \033[0;0m\n''')
    #     exit(0)

    # If hard drive exists, load it as a stream and load the directory data
    if os.path.isfile('fs.data'):
        with open('fs.data', 'r+b') as fileIn:
            # Loads tuple containing both Directory and bitarray objects
            dirAndBitArray= pickle.load(fileIn)
            currentDir = dirAndBitArray[0]
            bitArray = dirAndBitArray[1]
            user_data = dirAndBitArray[2]
    
    # Otherwise, create hard drive and root folder with parent set to None
    else:
        with open("fs.data","wb") as out:
            out.truncate(size)
            bitArray=bitarray(int(size/chunk_size))
            bitArray.setall(0)
            bitArray[0:dirChunks]=True
            currentDir = Directory('root', None)
            user_data = {}
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
  
    # Create scripts if they aren't already created
    # if not os.path.isdir("stdin-scripts") or not os.path.isdir("stdout-scripts"):
    #     scriptCreator()
    # threads=list()
    # for i in range(thr):
    #     thread=threading.Thread(target=run,args=(currentDir,f"script{i}.txt"))#Creating threads
    #     threads.append(thread)
    #     thread.start()
    # for thread in threads:
    #     thread.join()#waiting for threads to finish
    s=Server()
    s.acceptConn(run,currentDir)
    #print('\n\u001b[36m\033[1m\t\t*-------> All threads successfully completed <------- *\n\033[0;0m')