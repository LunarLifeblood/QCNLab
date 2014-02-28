import os

def getList(directory):  # Function to get a list of files in the directory
    listOfFiles = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            listOfFiles.append(os.path.join(root, file))
    return listOfFiles
        
def printList(alist): # Function to print a list
    for item in alist:
        print(item)

def askForDir(): # Function to ask the user for a directory input
    directory = input("What's the directory of the files?")
    directory = directory.replace('/', '\\')
    return directory

def createZeroedList(size):
    alist = []
    for i in range(0, size, 1):
        alist.append(0)
    return alist

