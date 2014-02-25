import os

listOfFiles = []
for root, dirs, files in os.walk("C:\\Users\\Christopher\\git\\QCNLab\\qcnlab"):
    for file in files:
        listOfFiles.append(os.path.join(root, file))
        
for item in listOfFiles:
    print(item)