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
    maximum=0
    minimum=0
    z=0
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
                valueList.append(functions.convert(cell[4]),volts,eSqH)
            while(True):
                
                for i in range (z, len(valueList), 1):#Start loop for at top value search
                    if((valueList[i+2]-valueList[i+1])>((valueList[i+1]-valueList[i]))):
                        Top = valueList[i+1]
                        j=i+1 #store index for last value assessed
                        for z in range (j, len(valueList), 1): #now carry on only looking for a much smaller increment size to give bottom of step
                            if (((valueList[z+2]-valueList[z+1])<=(valueList[z+1]-valueList[z]))-(35*10e-3)):
                                Bottom = valueList[z+2]
                                i=z+2 #store last index assessed
                                break #break out of loop so we can calc the step
                    if((functions.convert(Top-Bottom) >= eSqH)): #filtering out the accidental mini steps
                        stepListVoltageValues.append(Top-Bottom)
                        minimum = min(stepListVoltageValues) #analyzing for the max and min range of step sizes,
                        maximum = max(stepListVoltageValues)
                    else:
                        print("false step between " + str(j) +"-" + str(i)) #explaining where we miscalc a step to then assess for debug
        binSize = (maximum - minimum)/(numBins-1) #To be done after data set has been full analyzed, so once while loop is ended
        for i in range (0, len(stepListVoltageValues), 1):
            listOfBins[int(stepListVoltageValues[i]/numBins)] +=1
                
    fs = open(outputFile, "w") #make the histo
    halfBin = binSize/2
    for i, item in enumerate(listOfBins):
        fs.write((str((i*binSize)+halfBin))+","+str(item)+"\n")
    print("Output File created.")
    fs.close()
               