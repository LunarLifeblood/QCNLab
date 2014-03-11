import functions

# Opens the files to read the data
maximum = 0.0
minimum = 0.0
numBins = 0
volts = 0
eSqH = 0
binSize = 0.0
listOfBins = []
condData = []
timeData = []


def getValues(numberBins, voltReading, eSqHVal):
    global numBins, volts, eSqH
    numBins = numberBins+1 #Plus 1 to stop the max value exceeding the range of the bins
    volts = voltReading
    eSqH = eSqHVal
    
    

def formHistogram(outputFile, listOfDirs):
    global maximum, minimum, numBins, volts, eSqH, binSize, listofBins, condData, timeData
    fs = None
    listOfBins = functions.createZeroedList(numBins)
    listOfMinimums = functions.createZeroedList(len(listOfDirs))
    print("Reading in data...")
    # read through files and fine minimum/maximum data
    count = 0
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
            minTemp = 0
            maxTemp = 0
            for line in fs:
                cell = line.split(",")
                cell[4] = functions.convert(float(cell[4]), volts, eSqH)
                if float(cell[4]) > maximum:
                    maximum = float(cell[4])
                elif float(cell[4]) < minimum:
                    minimum = float(cell[4])
                if float(cell[4]) > maxTemp:
                    maxTemp = float(cell[4])
                elif float(cell[4]) < minTemp:
                    minTemp = float(cell[4])
            listOfMinimums[count] = abs(minTemp)
            count+=1
    print("Number of files opened: "+str(len(listOfDirs)))
    print("Min = "+str(minimum)+"     Max = "+str(maximum))
    binSize = (maximum-minimum)/(numBins-1)
    print("BinSize = "+str(binSize))
    
    #go through file sorting data
    for i in range(0, len(listOfDirs), 1):
        success = True
        try:
            fs = open(listOfDirs[i], "r")
            #print("Successfully opened "+directory)
        except:
            print("FAILED to open "+listOfDirs[i])
            success = False
        if success == True:
            #read file
            for line in fs:
                cell = line.split(",")
                condData.append(functions.convert(float(cell[4]), volts, eSqH))
                timeData.append(float(cell[3]))



            marker = 0
            lineBasis = 5 # accuracy of line
            startLoc = []
            lineGrads = []
            lineIntercepts = []
            while marker < (2500 - lineBasis):
                stripDataX = []
                stripDataY = []
                deviations = []
                for i in range (marker, marker+lineBasis, 1):
                    stripDataX.append(timeData[i])
                    stripDataY.append(condData[i])
                startLoc.append(marker)
                marker+=5
                lineGrads.append(functions.regressionFindB(stripDataX, stripDataY))
                lineIntercepts(functions.regressionFindA(stripDataX, stripDataY, lineGrads[-1]))
                while marker < 2500:
                    yReg = lineIntercepts[-1] + lineGrads[-1]*timeData[marker]
                    diffRegReal = abs(yReg - condData[marker])
                    if diffRegReal > 10: # FudgeFactor
                        deviations.append(marker)
                        if len(deviations) == 3: # sensitivity to change
                            marker-= 3
                            break
                        
                
                for i, gradient in enumerate(lineGrads):
                    if abs(gradient) < 1000:
                        if i != len(lineGrads)-1: # FudgeFactor
                            sumY = 0
                            for j in range (startLoc[i], startLoc[i+1], 1):
                                sumY += condData[j]
                            sumY = sumY/(startLoc[i] - startLoc[i+1])
                            listOfBins[int(float(sumY+abs(minimum))/(binSize))] += 1
                        
                        elif i == len(lineGrads)-1: # FudgeFactor
                            sumY = 0
                            for j in range (startLoc[i], 2500, 1):
                                sumY += condData[j]
                            sumY = sumY/(startLoc[i] - 2500)
                            listOfBins[int(float(sumY+abs(minimum))/(binSize))] += 1
                

                

            condData = []
            timeData =[]
                
    fs.close()
    
    #Estimate peaks
    baseAvg = functions.findBaselineAvg(listOfBins, numBins)
    peakData = functions.findpeaks(listOfBins, numBins, binSize, baseAvg)
    print("Calculating peaks...")
    peakXVal = []
    for peak in peakData:
        peakXVal.append(peak*binSize)
    print("Peaks found at ")
    print(peakXVal)

    
    #write results to a file
    fs = open(outputFile, "w")
    j = 0
    halfBin = binSize/2
    for i in range(0, numBins, 1):
        try:
            if peakData[j] == i:
                fs.write((str((i*binSize)-abs(minimum)+halfBin))+","+str(listOfBins[i])+",20,"+str(baseAvg[i])+"\n")
                j+=1
            else:
                fs.write((str((i*binSize)-abs(minimum)+halfBin))+","+str(listOfBins[i])+",0,"+str(baseAvg[i])+"\n")
        except:
            fs.write((str((i*binSize)-abs(minimum)+halfBin))+","+str(listOfBins[i])+",0,"+str(baseAvg[i])+"\n")
    print("Output File created.")
    fs.close()
