# pyfs

High Speeds SUPER Quality Python Filesystem

For file handling a directory structure is made using dictionaries within dictionaries to make a tree structure. Each directory has a dictionary of folders and a dictionary of files.

## Commands

```
ls to display available folders

mkdir [dirname] to create folder
rmdir [dirname] to remove a folder
mkfile [filename] to create a file
rmfile [filename] to remove a file

read [filename] to read from a file
write [filename] to write to a file

move [filename] [from] [to] [size] to move text within the file

cd [dirname] to enter the folder

Also, 'cd ..' returns to previous folder

exit to EXIT
```
For example:
```
root/folderB/a:mkdir example folder
root/folderB/a:ls
        <DIR>   example folder
                somefile.txt
                someotherfile.txt
root/folderB/a:cd example folder
root/folderB/a/example folder:
```