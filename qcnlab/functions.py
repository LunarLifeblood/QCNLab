import os

def getList(directory):  # Function to get a list of files in the directory
    listOfFiles = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            listOfFiles.append(os.path.join(root, file))
    return listOfFiles
        
def printList(alist):
    for item in alist:
        print(item)

def askForDir():
    directory = input("What's the directory of the files?")
    directory = directory.replace('/', '\\')
    return directory

