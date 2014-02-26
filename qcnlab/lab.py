import functions

listOfDirs = functions.getList(functions.askForDir())

fs = None
for directory in listOfDirs:
    success = True
    try:
        fs = open(directory, "r")
        print("Successfully opened "+directory)
    except:
        print("FAILED to open "+directory)
        success = False
    if success == True:
        #read file
        for line in fs:
            print(line)
    