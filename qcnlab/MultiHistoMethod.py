import functions

# Opens the files to read the data
maximum = 0.0
minimum = 0.0
numBins = 0
volts = 0
eSqH = 0
binSize = 0.0
listOfBins = []
listOfBins2 = []
listOfMinimums = []
halfBin = 0
shifts = []
#Function to go get the necessary values
def getValues(numberBins, voltReading, eSqHVal, minVal, maxVal, shiftList):
    global numBins, volts, eSqH, minimum, maximum, shifts
    numBins = numberBins+1 #Plus 1 to stop the max value exceeding the range of the bins
    volts = voltReading
    eSqH = eSqHVal
    minimum = minVal
    maximum = maxVal
    shifts = shiftList

#Function to calculate a histogram
def formHistogram(outputFile, listOfDirs):
    global maximum, minimum, numBins, volts, eSqH, binSize, listofBins,  listOfBins2, halfBin, shifts
    fs = None
    listOfBins = functions.createZeroedList(numBins)
    print("Number of files opened: "+str(len(listOfDirs)))
    print("Min = "+str(minimum)+"     Max = "+str(maximum))
    binSize = (maximum-minimum)/(numBins-1)
    halfBin = binSize/2
    print("BinSize = "+str(binSize))
    
    #go through file sorting data
    for i in range(0, len(listOfDirs), 1):
        success = True
        listOfBins2 = functions.createZeroedList(numBins)
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
                cell[4] = functions.convert(float(cell[4]), volts, eSqH) - shifts[i]
                #create histogram of the single file
                if cell[4] < 14 and cell[4] > 0.3:
                    listOfBins2[int(float(cell[4]+abs(minimum))/(binSize))] += 1
            
            #Estimate peaks
            baseAvg = functions.findBaselineAvg(listOfBins2, numBins)
            peakData = functions.findpeaks(listOfBins2, numBins, binSize, baseAvg)
            temp = []
            for i, peak in enumerate(peakData):
                if listOfBins2[peak] > 1:
                    temp.append(peak)
            peakData = temp
            peakXVal = []
            for peak in peakData:
                    peakXVal.append((peak*binSize)+halfBin - abs(minimum))
            #Add peaks to overall histogram
            for value in peakXVal:
                listOfBins[int(float(value+abs(minimum))/(binSize))] += 1                         
            
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
    for i in range(0, numBins, 1):
        try:
            if peakData[j] == i:
                fs.write((str((i*binSize)-abs(minimum)+halfBin))+","+str(listOfBins[i])+",100,"+str(baseAvg[i])+"\n")
                j+=1
            else:
                fs.write((str((i*binSize)-abs(minimum)+halfBin))+","+str(listOfBins[i])+",0,"+str(baseAvg[i])+"\n")
        except:
            fs.write((str((i*binSize)-abs(minimum)+halfBin))+","+str(listOfBins[i])+",0,"+str(baseAvg[i])+"\n")
    print("Output File created.")
    fs.close()

