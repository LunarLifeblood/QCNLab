import functions

numBins = 0
volts = 0
eSqH = 0

binSize = 0.0
listOfBins = []
diffSize = 5


def getValues(numberBins, voltReading, eSqHVal):
    global numBins, volts, eSqH
    numBins = numberBins+1 #Plus 1 to stop the max value exceeding the range of the bins
    volts = voltReading
    eSqH = eSqHVal

def writeDiffData(data, magnitude):
    fw = open("diffdata.csv", "w")
    magnitude = 0.1* magnitude
    for i, value in enumerate(data):
        if i != 0:
            if abs(value)<magnitude:
                fw.write(str(i)+","+str(value)+",0.5\n")
            else:
                fw.write(str(i)+","+str(value)+",0\n")
    fw.close()
    
def writeVoltages(value, count):
    fw = open("vals"+str(count)+".csv", "a")
    fw.write(str(value)+"\n")
    fw.close()
    
def shuffleListAlong(value, aList):
    aList.append(value)
    aList.reverse()
    aList.pop()
    aList.reverse()
    return aList
    
def formHistogram(outputFile, listOfDirs):
    global numBins, volts, eSqH, binSize, listOfBins
    listOfBins = functions.createZeroedList(numBins)
    dataBuffer = functions.createZeroedList(diffSize)
    fs = None
    for count, directory in enumerate(listOfDirs):
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
            maximum = 0
            minimum = 0
            for line in fs:
                cell = line.split(",")
                cell[4] = float(cell[4])
                writeVoltages(cell[4], count)
                if cell[4] > maximum:
                    maximum = cell[4]
                elif cell[4] < minimum:
                    minimum = cell[4]
                data.append(cell[4]-dataBuffer[0])
                print(dataBuffer)
                dataBuffer = shuffleListAlong(float(cell[4]), dataBuffer)
            '''    
            if abs(maximum) > abs(minimum):
                if(abs(maximum) < 1.67):
                    writeDiffData(data, abs(maximum))
            elif abs(maximum) < abs(minimum):
                writeDiffData(data, abs(minimum))
            else:
                print("UH OH!")
            '''    
            for i in range(0, len(data), 10):
                if i<len(data):
                    #writeVoltages(data[i])
                    pass
            
    print("finished")
    
    