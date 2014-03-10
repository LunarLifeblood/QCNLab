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
    z=3
    something = int(z/3)
    j=0
    Top=0
    Bottom=0
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
            #read file
            for line in fs:
                cell = line.split(",")
                cell[4] = functions.convert(float(cell[4]), volts, eSqH)
                if float(cell[4]) > maximum:
                    maximum = float(cell[4])
                elif float(cell[4]) < minimum:
                    minimum = float(cell[4])

    
    
    
    
    
    
    
    for directory in listOfDirs:
        success = True
        try:
            fs = open(directory, "r")
            #print("Successfully opened "+directory)
        except:
            print("FAILED to open "+directory)
            success = False
        if success == True:
            valueList = []
            for line in fs:
                cell = line.split(",")
                print(cell[4]+"   "+str(float(cell[4])))
                cell[4] = functions.convert(float(cell[4]), volts, eSqH)
                valueList.append(float(cell[4])) 
            for i in range (z, len(valueList), 1):#Start loop for at top value search
                Top=None
                if((valueList[i]-valueList[i-something])>((valueList[i-something]-valueList[i-2*something]))):
                    Bottom = None
                    Top = valueList[i-something]
                    j=i-something #store index for last value assessed
                    for z in range (j, len(valueList), 1): #now carry on only looking for a much smaller increment size to give bottom of step
                        if (((valueList[z]-valueList[z-something])<=((valueList[z-something]-valueList[z-2*something]))*(1-0))):
                            Bottom = valueList[z]
                         #store last index assessed
                            break #break out of loop so we can calc the step
                try: 
                    if(((Top-Bottom) >= eSqH)): #filtering out the accidental mini steps
                        stepListVoltageValues.append(Top-Bottom)
                    else:
                        #print("false step between " + str(j) +"-" + str(i)) #explaining where we miscalc a step to then assess for debug
                        print("nboithing")
                except:
                    print("Nout")
        #minimum = min(stepListVoltageValues) #analyzing for the max and min range of step sizes,
        #maximum = max(stepListVoltageValues)
        binSize = (maximum - minimum)/(numBins-1) #To be done after data set has been full analyzed, so once while loop is ended
        print("min = "+str(minimum)+"   max = "+str(maximum)+"   BinSize = "+str(binSize))
        print(functions.printList(stepListVoltageValues))
        for i in range (0, len(stepListVoltageValues), 1):
            listOfBins[int((stepListVoltageValues[i]-minimum)/binSize)] +=1
            #print(int((stepListVoltageValues[i]-minimum)/binSize))
                
    fs = open(outputFile, "w") #make the histo
    halfBin = binSize/2
    for i, item in enumerate(listOfBins):
        fs.write((str((i*binSize)+halfBin))+","+str(item)+"\n")
    print("Output File created.")
    fs.close()
               