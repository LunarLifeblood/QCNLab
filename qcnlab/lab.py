import functions

# Asks user for a directory then returns a list of all files in it
listOfDirs = functions.getList(functions.askForDir())

# Opens the files to read the data
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
    