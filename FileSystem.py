# pickle is used to store objects
import pickle
import math
import os.path
import sys
from bitarray import bitarray
chunk_size=256
size=1024*10


class FileSystem:

    def __init__(self, diskstream):      
      self.virtualHardDisk = diskstream
      self.bitArray=None

    def __del__(self):
      self.virtualHardDisk.close()
        
    def allocateFile(self):
      allocatedChunks = self.lookFreeSpace(1)
      for chunk in allocatedChunks:
        self.bitArray[chunk] = True
      return allocatedChunks

    def deallocateFile(self, chunks):

        for chunk in chunks:
            # go to address of each chunk
            self.virtualHardDisk.seek(chunk*chunk_size)
            # clear bits of bitarray for each chunk
            self.bitArray[chunk] = False
            # set all bytes of chunk to 0x00
            self.virtualHardDisk.write(bytes.fromhex('00'*chunk_size))

    def lookFreeSpace(self, chunks):
      i=0
      parts=list()
      for chunk in range(0, chunks):
        # Skip used chunks
        while(self.bitArray[i]==True):
          i+=1
        # Append unused chunks
        parts.append(i)
        i+=1
      return parts


    def Write_to_File(self, chunks, length, input):
        initial_seek=0
        # Check if file is written or not
        if len(chunks)>0:
          initial_seek=(chunks[0]*chunk_size)+length
          self.virtualHardDisk.seek(initial_seek)
          # Check if the size of our input is greater than the space we have left in the last chunk
        
        remainingSpace = (len(chunks) * chunk_size) - length
        if sys.getsizeof(input) > remainingSpace:
            # Here, input is bigger than the space we already have
            # Separate part of input that can fit in the space and write it
            self.virtualHardDisk.write(input[0:remainingSpace])
            # Write the rest just like a new file
            input = input[remainingSpace+1:len(input)+1]
            chunks_needed=math.ceil(len(input)/chunk_size)
            chunks+=self.lookFreeSpace(chunks_needed)
        else:
            # Here, input will fit in the space we already have
            self.virtualHardDisk.write(input)
            length += len(input)
            return chunks, length
        
        initial_write=0

        for chunk in chunks:
            # if chunk has already been completely written, ignore it
            if self.bitArray[chunk]==True:
                continue
            else:    
                self.bitArray[chunk]=True
                self.virtualHardDisk.seek(chunk*chunk_size)

            # If not last chunk, write entire chunk
            if chunk!=chunks[-1]:
                self.virtualHardDisk.write(input[initial_write:initial_write+chunk_size])
                length+=chunk_size
                initial_write+=chunk_size
            # Else write the remaining data from input into last chunk
            else:
                self.virtualHardDisk.write(input[initial_write:len(input)])
                length+=len(input)-initial_write
        return chunks, length


    def move_within_file(self,from_,to,size):
        self.virtualHardDisk.seek(from_)
        textBytes=self.virtualHardDisk.read(size)
        self.virtualHardDisk.seek(from_)
        empty=" "*int(size)
        empty=empty.encode('utf-8')
        self.virtualHardDisk.write(empty)
        self.virtualHardDisk.seek(to)
        self.virtualHardDisk.write(textBytes)
        print("Move Operation Completed!")
        


    def Read_from_File(self, chunks):
        outputString= ""
        print(chunks)
        for chunk in chunks:
            self.virtualHardDisk.seek(chunk*chunk_size)
            outputString+=self.virtualHardDisk.read(chunk_size).decode("utf-8").rstrip("\x00")
        print(len(outputString))
        return outputString
    def setBitArray(self,bitArray):
      self.bitArray=bitArray
    def getBitArray(self):
      return self.bitArray
