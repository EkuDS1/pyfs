# pickle is used to store objects
import pickle
import math
import os.path
import sys
from bitarray import bitarray
import threading

chunk_size=256
threadLocal = threading.local()

# FileSystem contains the file stream between the program and the disk file
# It also contains information on which chunks have been allocated
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

    # Returns an array of currently free chunks, given the number of chunks the caller wants
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
        #Calculates which chunk is [to] in
        inWhichChunk=math.floor(to/chunk_size)
        #StartingAddress of that chunk 
        startingChunkAddr=chunks[inWhichChunk]*chunk_size
        #Calculate [to]  relative to that starting Address
        toRelative=to-len(chunks[:inWhichChunk])*chunk_size
        #Physical Address of where user wants to write
        toPhysical=toRelative+startingChunkAddr
        
        lastChar=length
        additionalLength=0
        #If [to] is after lastCharacter then calculate the number of spaces in between
        if to>lastChar:
          additionalLength=to-lastChar

        chunkLength=(len(chunks)*chunk_size)
        #Remaining Space in last chunk
        remainingSpace=chunkLength-to

        if to<chunkLength:
          self.virtualHardDisk.seek(toPhysical)
          #If input fits in remaining space then fit it in 
          if len(input)<remainingSpace:
            self.virtualHardDisk.write(input)
            length+=len(input)+additionalLength
            return chunks,length
          else: #Else fit what it can in the space
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
        inWhichChunk=math.floor(length/chunk_size)
        if length%256==0:
            inWhichChunk-=1
        startingChunkAddr=chunks[inWhichChunk]*chunk_size
        lengthRelative=length-len(chunks[:inWhichChunk])*chunk_size
        lengthPhysical=lengthRelative+startingChunkAddr
        if len(chunks)>0:
          initial_seek=lengthPhysical
          self.virtualHardDisk.seek(initial_seek)
        
        # Check if the size of our input is greater than the space we have left in the last chunk
        remainingSpace = (len(chunks) * chunk_size) - length

        # Here, input is bigger than the space we already have
        if sys.getsizeof(input) > remainingSpace:
            # Check if we have enough extra chunks to allocate, otherwise handle exception
            chunks_needed=math.ceil(len(input[remainingSpace:])/chunk_size)
            try:
                chunks+=self.lookFreeSpace(chunks_needed)
            except IndexError:
                threadLocal.ioh.output("Error! No more space on disk for input. Please delete a file.")
                # Returns chunks and length of file as-is
                return chunks, length

            # Separate part of input that can fit in the last chunk and write it
            self.virtualHardDisk.write(input[0:remainingSpace])
            length+=len(input[0:remainingSpace])
            # Write the rest just like a new file
            input = input[remainingSpace:]

        # Here, input will fit in the space we already have
        else:   
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

        #Calculate in which chunk is [to] and [from]
        inWhichChunkTo=math.floor(to/chunk_size)
        startingChunkAddrTo=chunks[inWhichChunkTo]*chunk_size
        inWhichChunkFrom=math.floor(from_/chunk_size)
        startingChunkAddrFrom=chunks[inWhichChunkFrom]*chunk_size
        #Calculate address of [to] [from] relative to starting chunk 
        to_Relative=to-len(chunks[:inWhichChunkTo])*chunk_size
        from_Relative=from_-len(chunks[:inWhichChunkFrom])*chunk_size

        to_Physical=to_Relative+startingChunkAddrTo
        from_Physical=from_Relative+startingChunkAddrFrom

        additionalLength=0
        #If [to] is greater than last character then calculate number of spaces in between
        if(to>length):
          threadLocal.ioh.output(length)
          additionalLength=to-from_
          length+=additionalLength
        
        self.virtualHardDisk.seek(from_Physical)
        textBytes=self.virtualHardDisk.read(size)
        self.virtualHardDisk.seek(from_Physical)
        empty=" "*int(size)
        empty=empty.encode('utf-8')
        self.virtualHardDisk.write(empty)
        self.virtualHardDisk.seek(to_Physical)
        self.virtualHardDisk.write(textBytes)
        threadLocal.ioh.output("Move Operation Completed!")
        return length


    def Read_from_File(self, chunks):
        outputString=""
        threadLocal.ioh.output(chunks)
        #Go into their chunks and read complete chunks, strip the empty bytes.
        for chunk in chunks:
            self.virtualHardDisk.seek(chunk*chunk_size)
            outputString+=self.virtualHardDisk.read(chunk_size).decode("utf-8").rstrip("\x00")
        threadLocal.ioh.output("Length: {}".format(len(outputString)))
        return outputString

    def read_at(self,chunks,at, readSize):
        outputString= self.Read_from_File(chunks)
        #Call read and split into [at:size]
        outputString = outputString[at:readSize+1]

        threadLocal.ioh.output(len(outputString))
        return outputString


    #Setter
    def setBitArray(self,bitArray):
        self.bitArray=bitArray 
    #Getter        
    def getBitArray(self):
        return self.bitArray
