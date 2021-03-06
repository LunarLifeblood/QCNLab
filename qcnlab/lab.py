import functions
import OriginalMethod
import ChrisMethod
import HarrysMethod
import TomsMethod
import TomsMethodv2
import RecursiveMethod
import MultiHistoMethod
import StripGradient

listOfDirs = functions.getList(functions.askForDir())


numBins = 125
volts = 15.07
#volts = float(input("What is the voltage reading?"))
folder = "2"
e = 1.6e-19
h = 6.626e-34
eSqH = (2*e*e)/h
binSize = 0.0
minimum = 0
maximum = 0
shifts = []

def findMinAndMax(): # function to find the minimum and maximum across all of the data, and find how much each file needs to be shifted to reach 0
    global minimum, maximum, shifts
    fs = None
    print("Reading in data...")
    # read through files and find minimum/maximum data
    for i, directory in enumerate(listOfDirs):
        data = []
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
                if cell[4] < 0.3:
                    data.append(cell[4])
                if float(cell[4]) > maximum:
                    maximum = float(cell[4])
                elif float(cell[4]) < minimum:
                    minimum = float(cell[4])
            
            if len(data) > 20:
                avgData = 0
                for item in data:
                    avgData += item
                avgData = avgData/len(data)
                shifts.append(avgData)
            else:
                shifts.append(-10000)
 
    avgShift = 0 
    count = 0  
    for item in shifts:
        if item != -10000:
            avgShift += item
            count += 1

    avgShift = avgShift/count
    for i, item in enumerate(shifts):
        if item == -10000:
            shifts[i] = avgShift



findMinAndMax()



# Function Calls For Different Methods
'''
#ORIGINAL
print("~~Original Method ~~")
OriginalMethod.getValues(numBins, volts, eSqH, minimum, maximum, shifts)
OriginalMethod.formHistogram("original - Output -"+folder+".csv", listOfDirs)
'''
'''
#Harry's Method
print("~~Harry's Method ~~")
HarrysMethod.getValues(numBins, volts, eSqH, minimum, maximum, shifts)
HarrysMethod.formHistogram("Harry Output -"+folder+".csv", listOfDirs)
'''
'''
#Multiple Histogram Method
print("~~Multiple Histogram Method ~~")
MultiHistoMethod.getValues(numBins, volts, eSqH, minimum, maximum, shifts)
MultiHistoMethod.formHistogram("MultiHistoMethod - Output -"+folder+".csv", listOfDirs)
'''
'''
#The Amazing Tom's Magnificent Method
print("~~Tom's Method V1 ~~")
TomsMethod.getValues(numBins, volts, eSqH)
TomsMethod.formHistogram("Tom Output -"+folder+".csv", listOfDirs)
'''
'''
#The Amazing Tom's Magnificent Method Version 2
print("~~Tom's Method V2~~")
TomsMethodv2.getValues(numBins, volts, eSqH)
TomsMethodv2.formHistogram("Tom - output_v2 -"+folder+".csv", listOfDirs)
'''

#Recursive Method
print("~~Recursive Method ~~")
RecursiveMethod.getValues(numBins, volts, eSqH, minimum, maximum, shifts)
RecursiveMethod.formHistogram("Recursive - Output -"+folder+".csv", listOfDirs)

'''
#Strip Gradient
print("~~Strip Gradient Method ~~")
StripGradient.getValues(numBins, volts, eSqH, minimum, maximum, shifts)
StripGradient.formHistogram("StripGradient - Output -"+folder+".csv", listOfDirs)
'''


