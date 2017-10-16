import sys
import os


def returnListOfExistingMshNames():
    listOfNames = []
    originalWorkingDirectory = os.getcwd()
    try:
        os.chdir("/home/fenics/shared/murtazo/cloudnaca/msh")
    except  OSError:
        print("This was run on a system without cloudnaca/msh\n")
        return 
    for fileName in os.listdir("/home/fenics/shared/murtazo/cloudnaca/msh/"):
        if fileName.endswith('.msh'):
            listOfNames.append(fileName)
    
    os.chdir(originalWorkingDirectory)
    return listOfNames

def returnListOfMshNamesToBeCreated(angle_start, angle_stop, n_angles, n_nodes, n_levels):
    listOfNames = []
    anglediff=((int(angle_stop)-int(angle_start))/int(n_angles))
    for level in range(int(n_levels)):
        for i in range(int(n_angles)):
            angle=(int(angle_start) + int(anglediff)*(i+1))
            listOfNames.append("r" + str(level) + "a" + str(angle) + "n" + str(n_nodes))
    
    return listOfNames

def returnListOfMshToBeConverted(angle_start, angle_stop, n_angles, n_nodes, n_levels):
    existingAlready = returnListOfExistingMshNames()
    toBeCreated = returnListOfMshNamesToBeCreated(angle_start, angle_stop, n_angles, n_nodes, n_levels)
    listToBeConverted = []
    for name in toBeCreated:
        if not (name+".msh") in existingAlready:
            listToBeConverted.append(name)
    return listToBeConverted

if __name__ == '__main__':
    angle_start=sys.argv[1]
    angle_stop=sys.argv[2]
    n_angles=sys.argv[3]
    n_nodes=sys.argv[4]
    n_levels=sys.argv[5]
    print(returnListOfMshNamesToBeCreated(angle_start, angle_stop, n_angles, n_nodes, n_levels))