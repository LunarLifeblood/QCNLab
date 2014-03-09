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
condData = []
timeData = []
steps = []
recursionCount = 0
def getValues(numberBins, voltReading, eSqHVal):
    global numBins, volts, eSqH
    numBins = numberBins+1 #Plus 1 to stop the max value exceeding the range of the bins
    volts = voltReading
    eSqH = eSqHVal
    
def removeDuplicates(aList):
    previousItem = 0
    fixedList = []
    for i, item in enumerate(aList):
        if abs(item - previousItem) >= 0.00005:
            if i == 0:
                previousItem = item
                continue
            else:
                fixedList.append(previousItem)
        previousItem = item
      
    if aList[-1] != previousItem:
        fixedList.append(previousItem)
    fixedList.append(aList[-1])
    
    return fixedList

def removeMinMaxValues(aList):
    fixedList = []
    for item in aList:
        if item < 14 and item > 0.3:
            fixedList.append(item)
    return fixedList

def recursiveStepSearch(lower, upper, yData, xData):
    global steps, recursionCount
    recursionCount+=1
    mid = int((lower+upper)/2)
    if lower != mid and lower != mid-1 :
        averageLeft = 0
        averageRight = 0

        leftData = []
        rightData = []
        for i in range(lower, mid, 1):
            leftData.append(yData[i])
        for i in range(mid, upper+1, 1):
            rightData.append(yData[i])
        gradientLeft = functions.regressionFindB(xData, leftData)
        gradientRight = functions.regressionFindB(xData, rightData)
        print("lower = "+str(lower)+"    mid = "+str(mid)+"    upper = "+str(upper)+"    lower-mid = "+str(mid-lower))
        print("gradLeft = "+str(gradientLeft)+"      gradRight = "+str(gradientRight))
        if abs(gradientLeft - gradientRight) <= 11000:
            if abs(gradientRight) <= 5000 and abs(gradientLeft) <= 5000:
                for i in range(lower, mid, 1):
                    averageLeft+= yData[i]
                averageLeft = averageLeft/(mid-lower)
                for i in range(mid, upper+1, 1):
                    averageRight+= yData[i]
                averageRight = averageRight/((upper-mid)+1)
                print("averageLeft = "+str(averageLeft)+"     averageRight = "+str(averageRight)+"     diff = "+str(abs(averageLeft - averageRight)))
                if abs(averageLeft - averageRight) <= 0.3:
                    steps.append((averageLeft+averageRight)/2)
                else:
                    recursiveStepSearch(lower, mid, yData, xData)
                    recursiveStepSearch(mid, upper, yData, xData)
            else:
                recursiveStepSearch(lower, mid, yData, xData)
                recursiveStepSearch(mid, upper, yData, xData)
        elif lower == mid-1:
            print("woo!")
            averageLeft= yData[lower]
            for i in range(mid, upper+1, 1):
                averageRight+= yData[i]
            averageRight = averageRight/((upper-mid)+1)
            #print("averageLeft = "+str(averageLeft)+"     averageRight = "+str(averageRight))
            if abs(averageLeft - averageRight) <= 0.3:
                steps.append((averageLeft+averageRight)/2)
            else:
                recursiveStepSearch(lower, mid, yData, xData)
                recursiveStepSearch(mid, upper, yData, xData)
            
            
            
            
        else:
            recursiveStepSearch(lower, mid, yData, xData)
            recursiveStepSearch(mid, upper, yData, xData)
        

    
    

def formHistogram(outputFile, listOfDirs):
    global maximum, minimum, numBins, volts, eSqH, binSize, listofBins, listOfMinimums, condData, steps, timeData
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
            #fileName = "listOfConds 2 "+str(i)+".csv"
            #functions.writeList(fileName, condData)
            recursiveStepSearch(0, len(condData)-1, condData, timeData)
            #print(steps)
            steps = removeDuplicates(steps)
            steps = removeMinMaxValues(steps)
            print("Num steps: "+str(len(steps))+"      RecursionCount = "+str(recursionCount))
            print(steps)
            for item in steps:
                listOfBins[int(float(item+abs(minimum))/(binSize))] += 1
            steps = []
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
