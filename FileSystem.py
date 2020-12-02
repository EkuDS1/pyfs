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

    def write_at(self,chunks,length,input,to):
        StartingAddress=chunks[0]*chunk_size 
        finalWrite=StartingAddress+length
        to=StartingAddress+to
        additionalLength=0
        if to>finalWrite:
          additionalLength=to-finalWrite
        
        chunkLength=(len(chunks)*chunk_size)+StartingAddress
        remainingSpace=chunkLength-to
        
        if to<chunkLength:
          self.virtualHardDisk.seek(to)
          if len(input)<remainingSpace:
            self.virtualHardDisk.write(input)
            length+=len(input)+additionalLength
            return chunks,length
          else:
            self.virtualHardDisk.write(input[0:remainingSpace])
            length+=len(input[0:remainingSpace])
            # Write the rest just like a new file
            input = input[remainingSpace+1:len(input)+1]
            chunks_needed=math.ceil(len(input)/chunk_size)
            chunks+=self.lookFreeSpace(chunks_needed)

                
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
            length+=len(input[0:remainingSpace])
            # Write the rest just like a new file
            input = input[remainingSpace:]
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
                self.virtualHardDisk.write(input[initial_write:])
                length+=len(input)-initial_write
        return chunks, length


    def move_within_file(self,from_,to,size,chunks,length):
        startingAddress=chunks[0]*chunk_size
        finalWrite=startingAddress+length
        additionalLength=0
        if(to>finalWrite):
          print(finalWrite)
          additionalLength=to-from_
          length+=additionalLength
        
        self.virtualHardDisk.seek(from_)
        textBytes=self.virtualHardDisk.read(size)
        self.virtualHardDisk.seek(from_)
        empty=" "*int(size)
        empty=empty.encode('utf-8')
        self.virtualHardDisk.write(empty)
        self.virtualHardDisk.seek(to)
        self.virtualHardDisk.write(textBytes)
        print("Move Operation Completed!")
        return length


    def Read_from_File(self, chunks):
        outputString=""
        print(chunks)
        for chunk in chunks:
            self.virtualHardDisk.seek(chunk*chunk_size)
            outputString+=self.virtualHardDisk.read(chunk_size).decode("utf-8").rstrip("\x00")
        print("Length: {}".format(len(outputString)))
        return outputString

    def read_at(self,chunks,at, readSize):
        outputString=""
        startingAddress = chunks[0] * chunk_size
        at = at + startingAddress

        

        if at == startingAddress:
            firstChunk = math.ceil(at / chunk_size) + 1
        else:
            firstChunk = math.ceil(at / chunk_size)

        lastChunk = math.ceil((at + readSize)/chunk_size)

        self.virtualHardDisk.seek(at)
        
        # if we only need to read from one chunk
        if firstChunk == lastChunk:
            outputString+=self.virtualHardDisk.read(readSize).decode("utf-8").rstrip("\x00")
        # if we need to read from more than one chunk
        else:
            firstRead = chunk_size * firstChunk - at
            outputString+=self.virtualHardDisk.read(firstRead).decode("utf-8").rstrip("\x00")

            for chunk in chunks[firstChunk:lastChunk]:
                self.virtualHardDisk.seek(chunk*chunk_size)
                outputString+=self.virtualHardDisk.read(chunk_size).decode("utf-8").rstrip("\x00")
            
            lastRead = (chunk_size * lastChunk) - (at + readSize)
            outputString+=self.virtualHardDisk.read(lastRead).decode("utf-8").rstrip("\x00")

            

        print(len(outputString))
        return outputString



    def setBitArray(self,bitArray):
        self.bitArray=bitArray
        
    def getBitArray(self):
        return self.bitArray
