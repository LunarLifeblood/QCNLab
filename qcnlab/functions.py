import os

def getList(dir):  # Function to get a list of files in the directory
    listOfFiles = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            listOfFiles.append(os.path.join(root, file))
    return listOfFiles
        
def printList(list):
    for item in list:
        print(item)

def askForDir():
    dir = input("What's the directory of the files?")
    dir = dir.replace('/', '\\')
    print(dir)
    return dir