import functions
e = 1.6e-19
h = 6.626e-34
eSqH = (2*e*e)/h
listOfDirs = functions.getList(functions.askForDir())
numBins = 200
volts = 15.18
numBins += 1 #to account for max data value
listOfBins = functions.createZeroedList(numBins)
maximum = 0
minimum = 0
shifts = []

def findMinAndMax():
    global minimum, maximum, shifts, listOfDirs
    fs = None
    print("Reading in data...")
    # read through files and fine minimum/maximum data
    for i, directory in enumerate(listOfDirs):
        data = []
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
                cell[4] = functions.convert(float(cell[4]), volts, eSqH)
                if cell[4] < 0.3:
                    data.append(cell[4])
                if float(cell[4]) > maximum:
                    maximum = float(cell[4])
                elif float(cell[4]) < minimum:
                    minimum = float(cell[4])
            
            if len(data) > 0:
                avgData = 0
                for item in data:
                    avgData += item
                avgData = avgData/len(data)
                shifts.append(avgData)
            else:
                shifts.append(-10000)
 
    avgShift = 0 
    count = 0  
    for item in shifts:
        if item != -10000:
            avgShift += item
            count += 1

    avgShift = avgShift/count
    for i, item in enumerate(shifts):
        if item == -10000:
            shifts[i] = avgShift





findMinAndMax()
print("Reading in Data...")
data = []
for i, directory in enumerate(listOfDirs):
    fs = open(directory, "r")
    for line in fs:
        column = line.split(",")
        data.append(functions.convert(float(column[4]), volts, eSqH) - shifts[i])# <-----TOM make this one point to the correct column
    fs.close()
binSize = (maximum-minimum)/(numBins-1)
print("Sorting data...")
for item in data:
    if item < 14 and item > 0:
        listOfBins[int(float(item-minimum)/binSize)] += 1
print("Writing data...")
fs = open("somefile.csv", "w")
halfBin = binSize/2
for i, item in enumerate(listOfBins):
    fs.write(str((i*binSize) +halfBin+minimum)+","+str(item)+"\n")
print("Finished.")
fs.close()