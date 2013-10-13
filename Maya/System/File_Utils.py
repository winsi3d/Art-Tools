import os


def findAllFiles(fileDirectory, fileExtension):
    # Returns a list of all file names, excluding the file extension
    allFiles = os.listdir(fileDirectory)
    
    returnFiles = []
    
    for f in allFiles:
        splitString = str(f).rpartition(fileExtension)
        # rpartition() will split a string at the last place it finds whatever is in brackets
        # partition() will split a string at the first place it finds whatever is in brackets
        
        if not splitString[1] == "" and splitString[2] == "" and splitString[0] != "__init__":
            returnFiles.append(splitString[0])
            
            
    return returnFiles