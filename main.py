#impoting json as the file directory system is stored as json file
import json 

#global dictionary created to keep the track of directory
global previous_dict, i
previous_dict={}
i = 0

#to move back to parent directory
def to_parent_directory(i):
    
    #as pervious_dict contains the last enter directory
    #as it is moving to parent directory
    #current directory is changed to previous directory
    previous_dict[i] = {}
    i-=1
    print(previous_dict[i].keys())
    check_file(previous_dict[i], i)
        
 # It is to create folder in current directory
def create_folder(i,foldername_to_create):
    
    # it creates a empty dictionary for 
    # new folder in the curent directory
    previous_dict[i][foldername_to_create] = {}
    print(previous_dict[i].keys())
    
    #recall function
    check_file(previous_dict[i],i)

# It will delete the folder from directory only
def delete_folder(i, foldername_to_delete):
    del(previous_dict[i][foldername_to_delete])
    print(previous_dict[i].keys())
    check_file(previous_dict[i],i)

def create_file(i,filename_to_create):
    
    # it creates a empty file for 
    # new file in the curent directory
    # Store the address of file here
    ####################################################################################
    # EXAMPLE---------------------->
    previous_dict[i][filename_to_create] = {"start Address" : "0000", "End Address" : "0000", "Offset Address":"0000" }
    
    write_file(i, filename_to_create)
    ####################################################################################
    
    print(previous_dict[i].keys())
    #recall function
    check_file(previous_dict[i],i)
    
def write_file(i, filename_to_write):
    print("writing file")
    # line below contains the file address
    #previous_dict[i][filename_to_write]
    
    # text to be written in the file
    input_text = input ("Enter the text you want to write in this file")
    # Enter the text in main file
    
def read_file(i,file_to_read):    
    print("reading file")
    # Below this line there is a dictionary
    # which contains the address of file
    # previous_dict[i][file_to_read]
    

# function created to get into folders
# takes 2 input 
# first directory and index for keeping the track of directory
def check_file(dictt,i):

    folderName = input("Press 0 to create folder\nPress 1 to exit\nPress 00 to go back previous folder\nPress 3 to delete folder or file\nName the folder you want to enter: ")
    
    # To end the code 
    if folderName == "1":
        print("\n<<<----------------EXIT---------------->>>\n");
    # To get back to previous directory
    elif folderName == "00": 
        # if its not in main folders
        if i > 0:   
            to_parent_directory(i)
        # if its in main folder no need to call function
        elif i == 0:
            print("\n")
            print(dictt.keys())
            print("\n")
            # again to main function with parent directory as current directory
            check_file(dictt,i)
            
    # To create a folder in current directory
    elif folderName == "0":  
        foldername_to_create = input("Enter the name of folder: ")
        # adding 1 to store the current directory in other key
        i+=1
        create_folder(i,foldername_to_create)

    ## Deleting folder from directory
    elif folderName == "3":
        foldername_to_delete = input("Enter the folder name: ")
        delete_folder(i, foldername_to_delete)
        
    # Checking if the folder exists or not
    elif dictt.__contains__(folderName) :
        i+=1 
        previous_dict[i]= dictt[folderName]
        # check if text file arives only
        if len(dictt[folderName].values()) == 0:
            print("Folder is empty")
            
            #Creating new folder in an empty folder
            option4 = input("Press 1 to create folder\nPress 00 to go to parent directory: ")
            if option4 == "1":
                foldername_to_create = input("Enter the name of folder: ")
                create_folder(i,foldername_to_create)
            # moving to parent directory
            elif option4 == "00":
                to_parent_directory(i)
        
        else:        
            # Printing the folders that are in that folder
            print(dictt[folderName].keys())
            # Moving into the folder
            dictt = dictt[folderName]
 
            while (True):
                # Asking user if he wants to get into the folders or not or want to create a folder
                option3 = input("Press 00 to go to parent directory\nPress 0 to EXIT THE CODE\nPress 1 to create a folder:\nPress 2 if u want to enter the folder\nPress 3 to delete a folder or file: ")
                
                # to exit the code
                if option3 == "0":
                    break
                
                # Creating a folder in the directory present
                elif option3 == "1":
                    foldername_to_create = input("Enter the name of folder: ")
                    create_folder(i,foldername_to_create)
                    break
                    
                # Recalling the function 
                # if the user want to get into the folder or not
                elif option3 == "2":
                    check_file(dictt, i)
                    break
                
                # to move to parent directory
                elif option3 == "00":
                    to_parent_directory(i)
                    break  
                
                # to delete a folder
                elif option3 == "3":
                    foldername_to_delete = input("Enter the folder name: ")
                    delete_folder(i, foldername_to_delete)
                
    else :
        # folder doesnt exist
        print("folder dont exist\n")
        print(previous_dict[i].keys())
        check_file(previous_dict[i], i)
        
        
################################## Main Code starts from here ##################################
        
# Directories structure is taken 
# from json file to dictionary  
directories_structure = open("data.json")
dic = json.load(directories_structure)
    
while True: 
    
    # Printing the main folders
    print(dic.keys())
    input1 = input("Press 0 to create folder\nPress 1 to enter the folder\nPress 2 to EXIT: ")

    # Setting the current directory of the user as the main folders directory
    previous_dict[0]= dic
    
    # Creating a new folder/file
    if input1 == "0":
            foldername_to_create = input("Enter the name of folder: ")
            create_folder(i,foldername_to_create)
    
    # Going into the directory
    elif input1 == "1" :
        flag = 0
        check_file(dic, i)

    # Exiting the code
    elif input1 == "2":
      
        print("\n************ Program Closed ************")
        break

# Uodated directies stored back into json file
with open("data.json", "w") as outfile:  
    json.dump(dic, outfile) 