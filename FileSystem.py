import os
import sys
import pickle
from bitarray import bitarray
import math


class FileSystem:
    def __init__(self, size, chunk_size):
        self.dicn = dict()
        self.size = size
        self.chunk_size = chunk_size
        self.chunks = int(self.size/self.chunk_size)
        self.bitArray = bitarray(self.chunks)
        self.bitArray.setall(0)
        # Allocating 0th Chunk for File Descriptor
        
        self.dicn['FileDescriptorTable'] = 0
        self.dicn['bitArray'] = self.bitArray
        self.bitArray[0] = True

    def lookFreeSpace(self, chunks):
        i = 0
        parts = list()
        for chunk in range(chunks):
            while(self.bitArray[i] != False):
                i += 1
            self.bitArray[i] = True
            parts.append(i)
        return parts

    def createFile(self):
        virtualHardDisk = open("testfile", "r+b")
        parts = list()
        # File Data
        name = input("Please enter a File Name:")
        textBytes = input("Please enter the data you want to store:")
        # Convert String into Bytes to save
        textBytes = textBytes.encode("utf-8")
        # Function to calculate number of chunks needed to save this data
        chunks_needed = math.ceil(len(textBytes)/self.chunk_size)
        parts = self.lookFreeSpace(chunks_needed)
        initial_write = 0
        for part in parts:
            # Mark Allocated Space as true in Bitarray index
            self.bitArray[part] = True
            # Go to the free space chunk and write that data
            virtualHardDisk.seek((part*self.chunk_size))
            if(part == parts[-1]):
                # When stream is at last chunk, write the remaining data there
                virtualHardDisk.write(textBytes[initial_write:len(textBytes)])
            else:
                # If Streaming is not at last chunk then write an entire chunk
                virtualHardDisk.write(textBytes[initial_write:initial_write + self.chunk_size])
                initial_write += self.chunk_size
            self.dicn[name] = parts

    def readFile(self):
        name = input("Enter the file you want to open:")
        virtualHardDisk = open("testfile", "r+b")
        parts = self.dicn[name]
        print(parts)

        outputString = ""
        for part in parts:
            virtualHardDisk.seek(part*self.chunk_size)
            outputString += virtualHardDisk.read(self.chunk_size).decode("utf-8").rstrip("\x00")
        print(outputString)

    def dumpFile(self):
        # Save the objects in the 0th Chunk
        print(f'Directory data has size: {sys.getsizeof(self.dicn)}')
        fie = open("testfile", "r+b")
        dump = pickle.dumps(self.dicn, protocol=2)
        fie.write(dump)
        fie.close()


def readDump(fs):
  with open("testfile", "rb") as inputfie:
      # Load the file Descriptor.
      dicnx = pickle.load(inputfie)
      fs.dicn = dicnx
      # Initialize the bit Array to know which space is filled
      fs.bitArray = fs.dicn['bitArray']
      print(fs.dicn)


def createDisk(sizeinBytes):
    with open("testfile", "wb") as out:
        out.truncate(sizeinBytes)


if __name__ == "__main__":
    
    Fmds = FileSystem(10*1024, 256)
    
    # Create disk file if it doesn't exist
    if not os.path.isfile('testfile'):
        createDisk(10*1024)
    else:
        readDump(Fmds)
    
    #Fmds.createFile()
    Fmds.readFile()
    Fmds.dumpFile()
