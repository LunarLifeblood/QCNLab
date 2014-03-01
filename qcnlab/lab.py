import functions

# Asks user for a directory then returns a list of all files in it
listOfDirs = functions.getList(functions.askForDir())

# Opens the files to read the data
maximum = 0.0
minimum = 0.0
numBins = 250
binSize = 0.0
listOfBins = functions.createZeroedList(numBins)
fs = None
print("Reading in data...")
# read through files and fine minimum/maximum data
for directory in listOfDirs:
    success = True
    try:
        fs = open(directory, "r")
        #print("Successfully opened "+directory)
    except:
        print("FAILED to open "+directory)
        success = False
    if success == True:
        #read file
        for line in fs:
            cell = line.split(",")
            if float(cell[4]) > maximum:
                maximum = float(cell[4])
            elif float(cell[4]) < minimum:
                minimum = float(cell[4])
print("Min = "+str(minimum)+"     Max = "+str(maximum))
binSize = (maximum-minimum)/numBins

#go through file sorting data
for directory in listOfDirs:
    success = True
    try:
        fs = open(directory, "r")
        #print("Successfully opened "+directory)
    except:
        print("FAILED to open "+directory)
        success = False
    if success == True:
        #read file
        for line in fs:
            cell = line.split(",")
            listOfBins[int((float(cell[4])+abs(minimum))/binSize)-1] += 1
fs.close()
print("Finished.")
#write results to a file
fs = open("output.csv", "w")
for i in range(0, numBins, 1):
    fs.write((str((i*binSize)-abs(minimum)))+","+str(listOfBins[i])+"\n")
print("Output File created.")
fs.close()