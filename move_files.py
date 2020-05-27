"""
--- Author and How to Contribute to this ---
Code written by @codingdeck (Coding Deck) - Instagram Page for Programmers
Providing daily value content on Instagram
Add new features, fixes to this code and send it to @codingdeck on instagram
"""
# This code will move images, 

import os
import shutil # For moving files
import re # Regular Expressions

this_file_name = "move_files.py"

# Gettting current path
path = os.getcwd()

toMove = {
    'Images':{
        'folder':'Images',
        'extensions': ['png', 'jpeg', 'jpg', 'webp'],
    },
    'Videos':{
        'folder':'Videos',
        'extensions': ['mp4'],
    },
    'Compressed':{
        'folder':'Compressed',
        'extensions': ['rar', 'zip'],
    },
    'Misc':{
        'folder': 'Misc',
        'exclude': ['move_files.py'], # This should be the file name
        'is_misc': True,
    },
}
# Making necessary folders according to folder names given
# Getting all folderNames
folderNames = [i['folder'] for i in toMove.values()]


# Creating folders
for folderName in folderNames:
    newFolderPath = f"{path}/{folderName}"
    pathExists = os.path.exists(newFolderPath)
    if not pathExists:
        os.mkdir(newFolderPath)


def moveFiles(allFiles: list, source_dir: str, destination_dir: str):
    for fileName in allFiles:
        filePath = f"{source_dir}/{fileName}"
        destinationPath = f"{destination_dir}/{fileName}"

        # We will use this in the coming while loop
        
        if os.path.exists(destinationPath):
            # Index of the . before extension
            # Using reverse index
            dot_index = destinationPath.rindex('.')

            # For acting as numbers for the new file name - read more to understand it's usage
            max_duplicates = 100  # Maximum duplicates allowed for a file name
            indices = iter([i for i in range(1,max_duplicates)])

            while os.path.exists(destinationPath):
                # Create a new file name
                # Put a number in the file before .extension like (n)

                # First we get file path till .(Extension) then add the number index like '(n)', finally the .(Extension) is added
                try:
                    destinationPath = destinationPath[:dot_index] + f"({next(indices)})" + destinationPath[dot_index:]
                except:
                    # If max_duplicates exceeded rais this exception
                    raise Exception(f"Max duplicates allowed exceeded; max_duplicates = {max_duplicates}")
            
        # Move file on filePath to destinationPath
        shutil.move(filePath, destinationPath)
        print(f"Moved {filePath} to {destinationPath}")

def main(kwargs_dict):
    # Extracting dictionary contents
    folder = kwargs_dict.get('folder', "")
    exclude = kwargs_dict.get('exclude', [])
    is_misc = kwargs_dict.get('is_misc', False)
    extensions = kwargs_dict.get('extensions', [])

    # Get all the files
    allFiles = list(filter(os.path.isfile, os.listdir())) # Removes all folder and gets all files
    filteredFiles = [] # We will filter the files according to extensions

    print(folder, exclude, is_misc, extensions)


    # The Misc move files will move all the remaining file types to misc folder
    if is_misc:
        # Make sure this file isn't moved
        allFiles.remove(this_file_name)
        filteredFiles = allFiles
    
    # Get the files we want
    # Filter according to extensions
    
    for extension in extensions:
        filteredFiles.extend([fileName for fileName in allFiles if fileName.endswith(extension)]) # Adds files that endswith particular extensions

    # This function will move all files in source dir to destination dir
    moveFiles(allFiles=filteredFiles, source_dir=path, destination_dir=path+"/"+folder)



# Running moveFiles() for each type of files


# We finally move Misc files after others have finished executing
# main(toMove['Images'])

def all():
    for item in toMove.values():
        # We don't want the Misc files to be moved before others
        if item.get('is_misc', False):
            continue
        main(item)
    # Finally move the misc files
    main(toMove['Misc'])

# Run the code
all()

