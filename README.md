# pyfs - A Python File System / File Server

 A filesystem written in Python which can be logged into and used by multiple users. CRUD operations are implemented and text files can be manipulated in a multi-threaded environment. Users log in using their credentials. There is one "virtual hard disk" on which all users' files are stored. Usage given below.

For file handling a directory structure is made using dictionaries within dictionaries to make a tree structure. Each directory has a dictionary of folders and a dictionary of files.

## How to install/run

If you have pipenv installed, go to the root directory of the project in your terminal and run `pipenv install` to install dependencies.
Then simply run `python main.py` in the terminal.

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
