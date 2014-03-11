import functions
listOfDirs = functions.getList(functions.askForDir())
listOfBins = []
numBins = 200
for directory in listOfDirs:
    fs = open(directory, "r")
    data = []
    for line in fs:
        column = line.split(",")
        data.append(float(column[2]))# <-----TOM make this one point to the correct column
    fs.close()
    minimum = min(data)
    maximum = max(data)
    binSize = (maximum-minimum)/(numBins-1)
    for item in data:
        listOfBins[int((item+abs(minimum))/binSize)] += 1
    
fs = open("somefile.csv", "w")
halfBin = binSize/2
for i, item in enumerate(listOfBins):
    fs.write(str((i*binSize) +halfBin-abs(minimum))+","+str(item)+"\n")
