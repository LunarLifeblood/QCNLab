import functions
import OriginalMethod
import ChrisMethod
import HarrysMethod
import TomsMethod

listOfDirs = functions.getList(functions.askForDir())

numBins = 250
volts = 15.18
#volts = float(input("What is the voltage reading?"))
e = 1.6e-19
h = 6.626e-34
eSqH = (2*e*e)/h
binSize = 0.0
listOfBins = functions.createZeroedList(numBins)
listOfMinimums = functions.createZeroedList(len(listOfDirs))
'''
#ORIGINAL
OriginalMethod.getValues(numBins, volts, eSqH)
OriginalMethod.formHistogram("originaloutput.csv", listOfDirs)

#Chris' Method
ChrisMethod.getValues(numBins, volts, eSqH)
ChrisMethod.formHistogram("Chrisoutput.csv", listOfDirs)
'''
#Harry's Method
HarrysMethod.getValues(numBins, volts, eSqH)
HarrysMethod.formHistogram("Harryoutput.csv", listOfDirs)
'''
#ORIGINAL
TomsMethod.getValues(numBins, volts, eSqH)
TomsMethod.formHistogram("Tomoutput.csv", listOfDirs)
'''


