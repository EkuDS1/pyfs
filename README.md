# pyfs - A Python File System / File Server

 A filesystem written in Python which can be logged into and used by multiple users. CRUD operations are implemented and text files can be manipulated in a multi-threaded environment. Users log in using their credentials. There is one "virtual hard disk" on which all users' files and folders are stored. Usage given below.

## Introduction

This project was made for our Operating Systems course in our 5th Semester. The main motivation was for understanding the problems that come up when implementing a file system that is not only used by one person but many people and dealing with the intricate problems of multi-threading and synchronization.

## Technology Used

Python was our language of choice for this project. In part due to its ease of use and in part due to all the support that is available online.

The only module we needed was `bitarray`, which allows efficient manipulation of boolean values.

## Features

- Standard CRUD(Create Read Update Delete) operations on text files
- Manipulation of directories and moving files
- Allows multiple user clients to connect to a host file server and use the filesystem simultaneously
- View memory map of the filesystem

## Future Work and Evaluation

- An option to specify size of 'virtual hard disk'. By default, the max size is 1 KB.
- In order to allow clients to connect to the server, port forwarding may need to be set up. How this is set up may depend on the router that is being used by the server.

## How to Install/Run

Make sure you have pipenv installed. Go to the root directory of the project in your terminal and run `pipenv install` to install dependencies.

### To Run as a Server

Run `python main.py` in the terminal. You can set your IP and port in the `server.py` file. By default it is set to `localhost` at port 95.

### To Run as a Client

Run `python client.py`. You will be prompted to input the IP you wish to connect to. This will be the IP used by the server.  
You will then be asked to input your credentials if you have an account. If you do not have an account, you can create one. In either case, input a username and password.

## Commands and Example Usage

```text
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
```

For example:

```text
root/folderB/a:mkdir example_folder
root/folderB/a:ls
        <DIR>   example_folder
        <DIR>   another_folder
                somefile.txt
                someotherfile.txt
root/folderB/a:cd example_folder
root/folderB/a/example_folder: cd ../another_folder
root/folderB/a/another_folder
```

## Credits

- @EkuDS1 (Muhammad Rafay Nadeem)
- @Vin-Xi (Hamdan Rashid Siddiqui)
- @faraz455 (Muhammad Faraz Khan)
