import os

for i in range(10):
    with open(f"stdin-scripts/script{i}.txt",mode="w") as file:
        file.write(f"mkfile file{i}\n")
        file.write(f"open file{i}\n")
        file.write("write\n")
        file.write(f"Hamdan Rashid Is Here!\n")
        file.write("close\n")
        file.write("exit")

# for i in range(10):
#     os.remove(f"script{i}.txt")