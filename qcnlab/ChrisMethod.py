import functions

numBins = 0
volts = 0
eSqH = 0

binSize = 0.0
listOfBins = []


def getValues(numberBins, voltReading, eSqHVal):
    global numBins, volts, eSqH
    numBins = numberBins+1 #Plus 1 to stop the max value exceeding the range of the bins
    volts = voltReading
    eSqH = eSqHVal

def writeDiffData(data):
    fw = open("diffdata.csv", "w")
    for i, value in enumerate(data):
        fw.write(str(i)+","+str(value)+"\n")
    fw.close()
    
def formHistogram(outputFile, listOfDirs):
    global numBins, volts, eSqH, binSize, listOfBins
    listOfBins = functions.createZeroedList(numBins)
    fs = None
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
            data = []
            preCell = 0
            maximum = 0
            minimum = 0
            for line in fs:
                cell = float(line.split(","))
                
                data.append(cell[4]- preCell)
                preCell = float(cell[4])
            writeDiffData(data)
            
    
    