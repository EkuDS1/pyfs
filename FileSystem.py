import os
import pickle


class Node:
  def __init__(self):
    self.startingAddress=None
    self.offset=None
   
  def setOffset(self,offset):
    self.offset=offset

  def setStartingAddress(self,sA):
    self.startingAddress=sA

  def getOffset(self):
    return self.offset

  def getStartingAddress(self):
    return self.startingAddress
  
  def getLimit(self):
    return self.startingAddress+self.offset
  


class FileSystem:
  global dicn
  dicn=dict()
  def __init__(self): 
    dicn['initial_size']=128

  
  def createFile(self):
    node=Node()
    virtualHardDick=open("testfile","r+b")
    #File Data
    name=input("Please enter a File Name:")
    text=input("Please enter the data you want to store:")
    #Adding Node Info
    node.setStartingAddress(dicn['initial_size'])
    node.setOffset(len(text))
    #Adding Data to VirtualHardDisk
    dicn[name]=node
    virtualHardDick.seek(dicn['initial_size'])
    text=text.encode('utf-8')
    virtualHardDick.write(text)
    dicn['initial_size']+=len(text)
    

  def readFile(self):
    name=input("Enter the file you want to open")
    virtualHardDick=open("testfile","r+b")
    node=Node()
    node=dicn[name]
    startingAddress=node.getStartingAddress()
    virtualHardDick.seek(startingAddress)
    offset=node.getOffset()
    text=virtualHardDick.read(offset)
    text=text.decode('utf-8')
    print(text)


  def dumpFile(self):
    fie=open("testfile","r+b")
    dump=pickle.dumps(dicn,protocol=2)
    print(os.path.getsize("testfile"))
    fie.write(dump)
    print(len(dicn))
    print(len(dump))
    fie.close()

  def readDump(self):
    with open("testfile","rb") as inputfie:
      print(inputfie.read())
      inputfie.seek(0)
      dicnx=pickle.load(inputfie)
      print(dicnx)
      
def createDisk():
  with open("testfile","wb") as out:
    out.truncate(1024*1024)
    
if __name__=="__main__":
  createDisk()
  Fmds=FileSystem()
  Fmds.createFile()
  Fmds.readFile()

 