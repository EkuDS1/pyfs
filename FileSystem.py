import os
import pickle
from bitarray import bitarray
import math

class FileSystem:
  def __init__(self,size,chunk_size):     
    self.dicn=dict()  
    self.size=size
    self.chunk_size=chunk_size
    self.chunks=int(self.size/self.chunk_size)
    self.bitArray=bitarray(self.chunks)
    self.bitArray.setall(0)
    #Allocating 0th Chunk for File Descriptor
    self.dicn['FileDescriptorTable']=0
    self.dicn['bitArray']=self.bitArray
    self.bitArray[0]=True
    
    
  def lookFreeSpace(self,chunks):
    i=0
    parts=list()
    for chunk in range(1,chunks+1):
      while(self.bitArray[i]!=False):
        i+=1
      self.bitArray[i]=True
      parts.append(i)
    return parts

  def createFile(self):
    virtualHardDisk=open("testfile","r+b")
    parts=list()
    #File Data
    name=input("Please enter a File Name:")
    text=input("Please enter the data you want to store:")
    #Convert String into Bytes to save
    text=text.encode("utf-8")
    #Function to calculate number of chunks needed to save this data
    chunks_needed=math.ceil(len(text)/self.chunk_size)
    parts=self.lookFreeSpace(chunks_needed)
    initial_write=0
    for part in parts:
      #Mark Allocated Space as true in Bitarray index
      self.bitArray[part]=True
      #Go to the free space chunk and write that data
      virtualHardDisk.seek((part*self.chunk_size)+1)
      if(part==parts[-1]):
        #When stream is at last chunk, write the remaining data there
        virtualHardDisk.write(text[initial_write:len(text)])
      else:
        #If Streaming is not at last chunk then write 200 bytes
        virtualHardDisk.write(text[initial_write:self.chunk_size])
        initial_write+=self.chunk_size
      self.dicn[name]=parts
    
    
    

  def readFile(self):
    name=input("Enter the file you want to open:")
    virtualHardDisk=open("testfile","r+b")
    parts=self.dicn[name]
    print(parts)
    for part in parts:
      virtualHardDisk.seek((part*self.chunk_size)+1)
      print(virtualHardDisk.read(self.chunk_size).decode("ascii").rstrip("\x00"))
      

  def dumpFile(self):
    #Save the objects in the 0th Chunk
    fie=open("testfile","r+b")
    dump=pickle.dumps(self.dicn,protocol=2)
    fie.write(dump)
    fie.close()

  def readDump(self):
    with open("testfile","rb") as inputfie:
      #Load the file Descriptor.
      dicnx=pickle.load(inputfie)
      self.dicn=dicnx
      #Initialize the bit Array to know which space is filled
      self.bitArray=self.dicn['bitArray']
      print(self.dicn)
      
def createDisk():
  with open("testfile","wb") as out:
    out.truncate(1024*10)

if __name__=="__main__":
  
  #createDisk()
  Fmds=FileSystem(10*1024,200)
  Fmds.readDump()
  Fmds.createFile()
  Fmds.readFile()
  Fmds.dumpFile()
  