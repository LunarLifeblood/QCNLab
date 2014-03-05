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
    global numBins, volts, eSqH, binSize, listOfBins
    listOfBins = functions.createZeroedList(numBins)
    