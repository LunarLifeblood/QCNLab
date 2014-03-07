import functions

# Opens the files to read the data
maximum = 0.0
minimum = 0.0
numBins = 0
volts = 0
eSqH = 0
binSize = 0.0
prevcell = 0
listdiff = []
listdata = []
runningavg = []
listOfBins = []
listOfMinimums = []
markers = []
value = []
k = 0
kref=0
l=0
count2=0
total=0

def getValues(numberBins, voltReading, eSqHVal):
    global numBins, volts, eSqH
    numBins = numberBins+1 #Plus 1 to stop the max value exceeding the range of the bins
    volts = voltReading
    eSqH = eSqHVal

def formHistogram(outputFile, listOfDirs):
    global maximum, minimum, numBins, volts, eSqH, binSize, listofBins, listOfMinimums
    global prevcell, listdiff, listdata,value, runningavg, base, markers,k, total, count2, l, kref
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
                #if float(cell[4]) > maxTemp:
                   # maxTemp = float(cell[4])
                #elif float(cell[4]) < minTemp:
                 #   minTemp = float(cell[4])
            #listOfMinimums[count] = abs(minTemp)
            count = count + 1
    print("Number of files opened: "+str(len(listOfDirs)))
    #print("Min = "+str(minimum)+"     Max = "+str(maximum))
    binSize = (maximum-minimum)/(numBins-1)
    print("BinSize = "+str(binSize))
    
    #go through file sorting data
    for i in range(0, len(listOfDirs), 1):
        success = True
        try:
            fs = open(listOfDirs[i], "r")
            print("Successfully opened "+listOfDirs[i])
        except:
            print("FAILED to open "+listOfDirs[i])
            success = False
        if success == True:
            #read file
            prevcell = 0
            listdiff = []
            runningavg = []
            markers = []
            listData = []
            for line in fs:
                cell = line.split(",")
                cell[4] = functions.convert(float(cell[4]), volts, eSqH)
                listData.append(cell[4])
                #cell[4] = float(cell[4]) + float(listOfMinimums[i])
                #listOfBins[int(float(cell[4]+abs(minimum))/(binSize))] += 1
                listdiff.append((cell[4] - prevcell) / ( 4*10e-7 ) )
                prevcell = cell[4]                
            #fopen=open("c:\\Users\\Thomas\\Desktop\\QCNLab\\qcnlab\\New folder\\outputFile_" + str(i)+ ".csv","w")
            count=len(listdiff)
            for x in range (3,count-2,1):
                #fopen.write(str((listdiff[x-2]+listdiff[x-1]+listdiff[x]+listdiff[x+1]+listdiff[x+2])/5) + "\n")
                runningavg.append((listdiff[x-2]+listdiff[x-1]+listdiff[x]+listdiff[x+1]+listdiff[x+2])/5)
            #functions.writeList(listdiff,fopen)
            
            avg = sum(runningavg)/count
            base = ((avg)+min(runningavg))/2
            
            for x in range (1,count-5,1):
                if runningavg[x]<base:
                    markers.append(x)
            count=len(markers)
            k=markers[0]+1
            for x in range (0,count,1):
                if k!=markers[x]-1:
                    count2 = 0
                    total = 0
                    #print("HI")
                    for l in range (markers[x-1]+1,markers[x],1):
                        count2 = count2 + 1
                        total = listData[l]+total
                        #print("HELLO")
                    if count2>0:
                        #print("HOWDY")
                        value.append(total/count2)
                k=markers[x]
                
            #print(markers)
            
            #fopen.close()
    fs.close()
    
    minimum = 0
    maximum = max(value)
    print(maximum)
    
    binSize = (maximum)/(numBins-1)
    count=len(value)
    print(count)
    print(binSize)
    for i in range (0, count, 1):
        if value[i]>=0:
            listOfBins[int(value[i]/binSize)] += 1
            #print(int(value[i]/binsize))
        else:
            print("ERROR")
        
    #fopen=open("c:\\Users\\Thomas\\Desktop\\QCNLab\\qcnlab\\New folder\\outputFile.csv","w")
    fopen = open(outputFile, "w")
    
    for i in range (0,numBins,1):
    
        fopen.write(str((i*binSize)+(binSize/2))+","+str(listOfBins[i])+"\n")
    fopen.close()
    
    print("Finished.")
    '''    
    #Estimate peaks
    baseAvg = functions.findBaselineAvg(listOfBins, numBins)
    peakData = functions.findpeaks(listOfBins, numBins, binSize, baseAvg)
    print("Calculating peaks...")
    peakXVal = []
    for peak in peakData:
        peakXVal.append(peak*binSize)
    print("Peaks found at ")
    print(peakXVal)
'''
    '''
    #write results to a file
    fs = open(outputFile, "w")
    j = 0
    halfBin = binSize/2
    for i in range(0, numBins, 1):
        try:
            if peakData[j] == i:
                fs.write((str((i*binSize)-abs(minimum)+halfBin))+","+str(listOfBins[i])+",10000,"+str(baseAvg[i])+"\n")
                j+=1
            else:
                fs.write((str((i*binSize)-abs(minimum)+halfBin))+","+str(listOfBins[i])+",0,"+str(baseAvg[i])+"\n")
        except:
            fs.write((str((i*binSize)-abs(minimum)+halfBin))+","+str(listOfBins[i])+",0,"+str(baseAvg[i])+"\n")
    print("Output File created.")
    fs.close()'''

