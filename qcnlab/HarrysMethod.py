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
    
def formHistogram(outputFile, listOfDirs):
    valueList = []
    stepListVoltageValues = []
    fs = None
    global numBins, volts, eSqH, binSize, listOfBins
    listOfBins = functions.createZeroedList(numBins)
    for directory in listOfDirs:
        success = True
        try:
            fs = open(directory, "r")
            #print("Successfully opened "+directory)
        except:
            print("FAILED to open "+directory)
            success = False
        if success == True:
            for line in fs:
                cell = line.split(",")
                functions.convert(valueList.append(cell[4]))
            for i in range (0, len(valueList), 1):
                if((valueList[i+2]-valueList[i+1])>((valueList[i+1]-valueList[i]))):
                    Top = valueList[i+1]
                elif(((valueList[i+2]-valueList[i+1])<=(valueList[i+1]-valueList[i]))-(20*10e-3)):
                    Bottom = valueList[i+2]
                if((functions.convert(Top-Bottom) >= eSqH)):
                    stepListVoltageValues.append(Top-Bottom)
                    minimum = min(stepListVoltageValues)
                    maximum = max(stepListVoltageValues)
                else:
                    print("I love Chris")
            binSize = (maximum - minimum)/(numBins-1)
            for i in range (0, len(stepListVoltageValues), 1):
                listOfBins[int(stepListVoltageValues[i]/numBins)] +=1
                
    fs = open(outputFile, "w")
    halfBin = binSize/2
    for i, item in enumerate(listOfBins):
        fs.write((str((i*binSize)+halfBin))+","+str(item)+"\n")
    print("Output File created.")
    fs.close()
               