import os
import runme
from WorkerTasks import runAirfoilOnWorker

def meshmaker(one,two,three,four,five):
    os.chdir("/home/fenics/shared/murtazo/cloudnaca/")
    os.system("pwd")
    stringToCall = "./runme.sh " + str(one) + " " +  str(two) +" " + str(three) + " " + str(four) + " " + str(five) + ""
    os.system(stringToCall)

def xmlConverter():
    os.chdir("/home/fenics/shared/murtazo/cloudnaca/msh/")
    for fileName in os.listdir("/home/fenics/shared/murtazo/cloudnaca/msh/"):
        if fileName.endswith('.msh'):
            os.system("dolfin-convert " + fileName + " " + fileName[:-4] + ".xml")
            os.system("rm " + fileName)


def runAirfoil(filetoRun):
    os.chdir("/home/fenics/shared/murtazo/cloudnaca/msh/")
    wholeDamnXmlDict = {"filename" : filetoRun, "content" : ""}
    with open(filetoRun, "r") as xmlFile:
        wholeDamnXmlDict["content"] = xmlFile.read()
    results = runAirfoilOnWorker.delay(wholeDamnXmlDict)
    print(results.get())
    
def commandAirfoilPreCheck()
#
# The command that runs our whole service.
#
def receiveCommandAirfoil(angle_start, angle_stop, n_angles, n_nodes, n_levels):
    namesToCreate = returnListOfMshNamesToBeCreated(angle_start, angle_stop, n_angles, n_nodes, n_levels)
    mshToBeConverted = returnListOfMshToBeConverted(namesToCreate)
    if not mshToBeConverted:
        #no work to do all xmls have been runAirfoil instead return saved results
        
        

def receiveCommandAirfoilWithExtraParameters(angle_start, angle_stop, n_angles, n_nodes, n_levels, samples, viscosity, speed, time):

    runAirfoil("missingFile")

if __name__ == '__main__':
    one = (input("What is the first parameter?\n"))
    two = (input("What is the second parameter?\n"))
    three = (input("What is the third parameter?\n"))
    four = (input("What is the fourth parameter?\n"))
    five = (input("What is the fifth parameter?\n"))
    receiveCommandAirfoil(one,two,three,four,five)
    