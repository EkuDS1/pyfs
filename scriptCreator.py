import os

#Create input scripts to test threads, the user must first create
#folder stdin-scripts and stdout-scripts then run this code
#to create the input script.

if not os.path.isdir("stdin-scripts"):
    os.system("mkdir stdin-scripts")
if not os.path.isdir("stdout-scripts"):
    os.system("mkdir stdout-scripts")
    
for i in range(10):
    with open(f"stdin-scripts/script{i}.txt",mode="w") as file:
        file.write(f"mkfile file{i}\n")
        file.write(f"open file{i}\n")
        file.write("write\n")
        file.write(f"Hamdan Rashid Is Here!\n")
        file.write("read\n")
        file.write("close\n")
        file.write("exit")
    #Create files to output the thread into.s
    with open(f"stdout-scripts/script{i}.txt",mode="w") as file:
        pass
# for i in range(10):
#     os.remove(f"stdin-scripts/script{i}.txt")