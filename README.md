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
mvfile [filename] [path] to move file to another folder
cd [dirname] to enter the folder
Also, 'cd ..' returns to previous folder

memmap to view memory map of the filesystem

exit to EXIT
```
For example:
```
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