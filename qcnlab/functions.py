import os
import copy
import math

def getList(directory):  # Function to get a list of files in the directory
    listOfFiles = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            listOfFiles.append(os.path.join(root, file))
    return listOfFiles
        
def printList(alist): # Function to print a list
    for item in alist:
        print(item)
        
def writeList(output, alist):
    fs = open(output, "w")
    for item in alist:
        fs.write(str(item)+"\n")
    fs.close

def askForDir(): # Function to ask the user for a directory input
    directory = input("What's the directory of the files?")
    directory = directory.replace('/', '\\')
    return directory

def createZeroedList(size): # Creates a list filled with 0
    alist = []
    for i in range(0, size, 1):
        alist.append(0)
    return alist

def convert(value, volts, eSqH):
    #value = float(value)/100
    #value = ((float(value)/10e2)/volts)/eSqH
    
    value = (value*100)/10e5
    value = value/(volts*10e-3)
    value = value/eSqH
    
    #value = (eSqH*10e5*volts)*float(value)
    
    return value

def regressionFindA(xList, yList, b):
    sumX = sumY = 0
    for xVal, yVal in zip(xList, yList):
        sumX += xVal
        sumY += yVal
    a = (sumY/len(yList)) - (b*(sumX/len(yList)))
    return a

def regressionFindB(xList, yList):
    sumXX = sumX = sumY = sumXY = 0
    for xVal, yVal in zip(xList, yList):
        sumXX += math.pow(xVal, 2)
        sumX += xVal
        sumY += yVal
        sumXY += (xVal*yVal)
    sxx = sumXX - math.pow(sumX, 2)/len(yList)
    sxy = sumXY - (sumX*sumY)/len(yList)
    b = sxy/sxx
    return b

def findBaselineAvg(listOfBins, numBins): # Averages values in a list once, and then again ignoring 
    average = 0;
    for dataPoint in listOfBins:
        average += dataPoint
    average = average/numBins
    
    average2 = 0;
    for dataPoint in listOfBins:
        if dataPoint < average:
            average2 += dataPoint
        else:
            average2 += average
    average2 = average2/numBins
    
    average3 = 0;
    for dataPoint in listOfBins:
        if dataPoint < average2:
            average3 += dataPoint
        else:
            average3 += average2
    average3 = average3/numBins
    
    baseLine = copy.copy(listOfBins)
    avgSize = 15 # must be odd
    for i in range (0, int((avgSize-1)/2), 1):
        baseLine.append(0)
    baseLine.reverse()
    for i in range (0, int((avgSize-1)/2), 1):
        baseLine.append(0)
    baseLine.reverse()

        
    for i in range (int((avgSize-1)/2), numBins+int((avgSize-1)/2), 1):
        sum = 0
        for j in range (int(-(avgSize-1)/2), int(((avgSize-1)/2)+1), 1):
            sum += baseLine[i+j]
        baseLine[i] = sum/avgSize

    
    baseLine.reverse()
    for i in range (0, int((avgSize-1)/2), 1):
        baseLine.pop()
    baseLine.reverse()
    for i in range (0, int((avgSize-1)/2), 1):
        baseLine.pop()
    
    for i in range (0, numBins, 1):
        if baseLine[i] > listOfBins[i]:
            baseLine[i] = listOfBins[i]




    baseLine2 = copy.copy(baseLine)

    for i in range (0, int((avgSize-1)/2), 1):
        baseLine2.append(0)
    baseLine2.reverse()
    for i in range (0, int((avgSize-1)/2), 1):
        baseLine2.append(0)
    baseLine2.reverse()

        
    for i in range (int((avgSize-1)/2), numBins+int((avgSize-1)/2), 1):
        sum = 0
        for j in range (int(-(avgSize-1)/2), int(((avgSize-1)/2)+1), 1):
            sum += baseLine2[i+j]
        baseLine2[i] = sum/avgSize
    
    baseLine2.reverse()
    for i in range (0, int((avgSize-1)/2), 1):
        baseLine2.pop()
    baseLine2.reverse()
    for i in range (0, int((avgSize-1)/2), 1):
        baseLine2.pop()
    
    for i in range (0, numBins, 1):
        if baseLine2[i] > baseLine[i]:
            baseLine2[i] = baseLine[i]




    for i in range (0, numBins, 1):
        baseLine2[i] = (baseLine2[i] + average3)/2







    
    return baseLine2

def findpeaks(aList, size, binWidth, avg): # return the peak values
    data = []
    peaks = []
    for dataPoint in aList:
        data.append(float(dataPoint))
        
    for i in range(0, size-2, 1):
        if data[i] < data[i+1]:
            if data[i+1] >data[i+2]:
                if data[i+1] > 2*avg[i+1]:
                    #print("Peak found at or nearby: "+str((i+1)*binWidth))
                    peaks.append(i+1)

    return peaks