import os
import sys
import runme
import time
from WorkerTasks import runAirfoilOnWorker

def meshmaker(one,two,three,four,five):
    os.chdir("/home/fenics/shared/murtazo/cloudnaca/")
    os.system("pwd")
    with open("filesMade.txt", "a+") as file:
        namesToCreate = runme.returnListOfMshNamesToBeCreated(one, two, three, four, five)
        mshToBeConverted = runme.returnListOfMshToBeConverted(namesToCreate)
        for name in mshToBeConverted:
            file.write(name + "\n")
        
    stringToCall = "./runme.sh " + str(one) + " " +  str(two) +" " + str(three) + " " + str(four) + " " + str(five) + ""
    os.system(stringToCall)

def xmlConverter():
    os.chdir("/home/fenics/shared/murtazo/cloudnaca/msh/")
    for fileName in os.listdir("/home/fenics/shared/murtazo/cloudnaca/msh/"):
        if fileName.endswith('.msh'):
            os.system("dolfin-convert " + fileName + " " + fileName[:-4] + ".xml")
            os.system("rm " + fileName)
    os.sytem("rm " + "../geo" + " *")

def xmlConverterList(list):
    os.chdir("/home/fenics/shared/murtazo/cloudnaca/msh/")
    #print("echo ls -l " + "../geo")
    for fileName in list:
        print(fileName)
        #if fileName.endswith('.msh'):
        #print("dolfin-convert " + fileName + ".msh" + " " + fileName + ".xml")
        os.system("dolfin-convert " + fileName + ".msh" + " " + fileName + ".xml")
        os.system("rm " + fileName + ".msh")


#fileToRun should probably end with .xml
def runAirfoil(filetoRun):
    os.chdir("/home/fenics/shared/murtazo/cloudnaca/msh/")
    wholeDamnXmlDict = {"filename" : filetoRun, "content" : ""}
    with open(filetoRun, "r") as xmlFile:
        wholeDamnXmlDict["content"] = xmlFile.read()
    return runAirfoilOnWorker.delay(wholeDamnXmlDict)

#should add ".xml" to end of every name in listOfFiles in this function
def returnResultsOfFiles(listOfFileNames):
    returnString = ""
    for name in listOfFileNames:
        returnString = returnString + "/home/fenics/shared/results/" + name + ".res\n"
    return returnString
#
# The command that runs our whole service.
#
def deleteFilesInFolder():
    try:
        for fileName in os.listdir("/home/fenics/shared/murtazo/cloudnaca/geo"):
            os.remove("/home/fenics/shared/murtazo/cloudnaca/geo/" + fileName)
    except OSError:
        pass
    try:
        for fileName in os.listdir("/home/fenics/shared/murtazo/cloudnaca/msh"):
            os.remove("/home/fenics/shared/murtazo/cloudnaca/msh/" + fileName)
    except OSError:
        pass
    try:
        for fileName in os.listdir("/home/fenics/shared/results"):
            os.remove("/home/fenics/shared/results/" + fileName)
    except OSError:
        pass

def receiveCommandAirfoil(angle_start, angle_stop, n_angles, n_nodes, n_levels, deleteFiles):
    if(deleteFiles):
        deleteFilesInFolder()
    namesToCreate = runme.returnListOfMshNamesToBeCreated(angle_start, angle_stop, n_angles, n_nodes, n_levels)
    mshToBeConverted = runme.returnListOfMshToBeConverted(namesToCreate)
    #print(namesToCreate)
    #print(x)
    #print(mshToBeConverted)
    if mshToBeConverted:
        os.system("rm " + "/home/fenics/shared/murtazo/cloudnaca/geo/" + "*")
        os.chdir("/home/fenics/shared/murtazo/cloudnaca/msh/")
        os.system("rm *.msh")
        os.chdir("/home/fenics/shared/")
        meshmaker(angle_start, angle_stop, n_angles, n_nodes, n_levels) #todo xml convert
        #print(os.listdir("/home/fenics/shared/murtazo/cloudnaca/geo/"))
        xmlConverterList(mshToBeConverted)
    
    airfoilResultList = []
    for fileName in mshToBeConverted:
        airfoilResultList.append(runAirfoil(fileName + ".xml"))
    #os.system("rm " + "/home/fenics/shared/murtazo/cloudnaca/geo/" + "*")
    for result in airfoilResultList:
        while(not result.ready()):
            time.sleep(.1)
        content = result.get()
        with open("/home/fenics/shared/results/" + content[1][:-4] + ".res", "w+") as file:
            file.write(content[0])
        
    print(returnResultsOfFiles(namesToCreate))
    
    
        
        

def receiveCommandAirfoilWithExtraParameters(angle_start, angle_stop, n_angles, n_nodes, n_levels, samples, viscosity, speed, time):

    runAirfoil("missingFile")

if __name__ == '__main__':
    one=sys.argv[1]
    two=sys.argv[2]
    three=sys.argv[3]
    four=sys.argv[4]
    five=sys.argv[5]
    delete = False
    if len(sys.argv) > 6:
        if sys.argv[6] == "-d":
            delete = True
    #one = (input("What is the first parameter?\n"))
    #two = (input("What is the second parameter?\n"))
    #three = (input("What is the third parameter?\n"))
    #four = (input("What is the fourth parameter?\n"))
    #five = (input("What is the fifth parameter?\n"))
    receiveCommandAirfoil(one,two,three,four,five, delete)
    