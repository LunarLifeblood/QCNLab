import functions

# Opens the files to read the data
maximum = 0.0
minimum = 0.0
numBins = 0
volts = 0
eSqH = 0
binSize = 0.0
listOfBins = []
listOfMinimums = []

def getValues(numberBins, voltReading, eSqHVal, minVal, maxVal, shiftList):
    global numBins, volts, eSqH, minimum, maximum, shifts
    numBins = numberBins+1 #Plus 1 to stop the max value exceeding the range of the bins
    volts = voltReading
    eSqH = eSqHVal
    minimum = minVal
    maximum = maxVal
    shifts = shiftList

def formHistogram(outputFile, listOfDirs):
    global maximum, minimum, numBins, volts, eSqH, binSize, listofBins
    fs = None
    listOfBins = functions.createZeroedList(numBins)
    # read through files and fine minimum/maximum data
    print("Number of files opened: "+str(len(listOfDirs)))
    print("Min = "+str(minimum)+"     Max = "+str(maximum))
    binSize = (maximum-minimum)/(numBins-1)
    print("BinSize = "+str(binSize))
    
    #go through file sorting data
    for i in range(0, len(listOfDirs), 1):
        success = True
        try:
            fs = open(listOfDirs[i], "r")
            #print("Successfully opened "+listOfDirs[i])
        except:
            print("FAILED to open "+listOfDirs[i])
            success = False
        if success == True:
            #read file
            for line in fs:
                cell = line.split(",")
                cell[4] = functions.convert(float(cell[4]), volts, eSqH) - shifts[i]
                #cell[4] = float(cell[4]) + float(listOfMinimums[i])
                if cell[4] < 14 and cell[4] > 0:
                    listOfBins[int(float(cell[4]-minimum)/(binSize))] += 1
    fs.close()
    print("Finished.")
    
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
                fs.write((str((i*binSize)+minimum+halfBin))+","+str(listOfBins[i])+",10000,"+str(baseAvg[i])+"\n")
                j+=1
            else:
                fs.write((str((i*binSize)+minimum+halfBin))+","+str(listOfBins[i])+",0,"+str(baseAvg[i])+"\n")
        except:
            fs.write((str((i*binSize)+minimum+halfBin))+","+str(listOfBins[i])+",0,"+str(baseAvg[i])+"\n")
    print("Output File created.")
    fs.close()

