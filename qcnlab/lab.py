import functions
import OriginalMethod
import ChrisMethod
import HarrysMethod
import TomsMethod
import RecursiveMethod
import MultiHistoMethod

#listOfDirs = functions.getList(functions.askForDir())
listOfDirs = functions.getList("c:\\Users\\Thomas\\Desktop\\QCN\\4\\")

numBins = 125
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
<<<<<<< HEAD
#ORIGINAL
TomsMethod.getValues(numBins, volts, eSqH)
TomsMethod.formHistogram("Tomoutput.csv", listOfDirs)
'''
#Multiple Histogram Method
MultiHistoMethod.getValues(numBins, volts, eSqH)
MultiHistoMethod.formHistogram("MultiHistoMethod - Output.csv", listOfDirs)
=======
#The Amazing Tom's Magnificent Method
TomsMethod.getValues(numBins, volts, eSqH)
TomsMethod.formHistogram("Tomoutput.csv", listOfDirs)

>>>>>>> TomsMethod


#Recursive Method
RecursiveMethod.getValues(numBins, volts, eSqH)
RecursiveMethod.formHistogram("Recursive - Output.csv", listOfDirs)
