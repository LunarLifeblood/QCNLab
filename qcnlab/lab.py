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
#listOfDirs = functions.getList("c:\\Users\\Thomas\\Desktop\\QCN\\4\\")

numBins = 125
volts = 15.18
#volts = float(input("What is the voltage reading?"))
e = 1.6e-19
h = 6.626e-34
eSqH = (2*e*e)/h
binSize = 0.0
minimum = 0
maximum = 0

def findMinAndMax():
    global minimum, maximum
    fs = None
    print("Reading in data...")
    # read through files and fine minimum/maximum data
    for i, directory in enumerate(listOfDirs):
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




findMinAndMax()


'''
#ORIGINAL
OriginalMethod.getValues(numBins, volts, eSqH)
OriginalMethod.formHistogram("originaloutput.csv", listOfDirs)
'''
'''
#Chris' Method
ChrisMethod.getValues(numBins, volts, eSqH)
ChrisMethod.formHistogram("Chrisoutput.csv", listOfDirs)
'''
'''
#Harry's Method
HarrysMethod.getValues(numBins, volts, eSqH)
HarrysMethod.formHistogram("Harryoutput.csv", listOfDirs)
'''
'''
#Multiple Histogram Method
MultiHistoMethod.getValues(numBins, volts, eSqH)
MultiHistoMethod.formHistogram("MultiHistoMethod - Output.csv", listOfDirs)
'''
'''
#The Amazing Tom's Magnificent Method
TomsMethod.getValues(numBins, volts, eSqH)
TomsMethod.formHistogram("Tomoutput.csv", listOfDirs)
'''
'''
#The Amazing Tom's Magnificent Method Version 2
TomsMethodv2.getValues(numBins, volts, eSqH)
TomsMethodv2.formHistogram("Tomoutput_v2.csv", listOfDirs)
'''
'''
#Recursive Method
RecursiveMethod.getValues(numBins, volts, eSqH)
RecursiveMethod.formHistogram("Recursive - Output.csv", listOfDirs)
'''

#Strip Gradient
StripGradient.getValues(numBins, volts, eSqH, minimum, maximum)
StripGradient.formHistogram("StripGradient - Output.csv", listOfDirs)



