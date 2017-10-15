import subprocess
import os
one = (input("What is the first parameter?\n"))
two = (input("What is the second parameter?\n"))
three = (input("What is the third parameter?\n"))
four = (input("What is the fourth parameter?\n"))
five = (input("What is the fifth parameter?\n"))

def meshmaker(one,two,three,four, five):
    os.chdir("/home/fenics/shared/murtazo/cloudnaca/")
    os.system("pwd")
    os.system("./runme.sh " + one + " " +  two +" " + three + " " +  four + " " + five)
    print("kom vi hit")

def xmlConverter():
    os.chdir("/home/fenics/shared/murtazo/cloudnaca/msh/")
    for fileName in os.listdir("/home/fenics/shared/murtazo/cloudnaca/msh/"):
        if fileName.endswith('.msh'):
            os.system("dolfin-convert " + fileName + " " + fileName[:-4] + ".xml")

filetoRun = "r2a9n200.xml"
def runAirfoil(filetoRun):
    os.chdir("/home/fenics/shared/murtazo/navier_stokes_solver/")
    os.system("./airfoil 10 0.0001 10 0.005 ../cloudnaca/msh/" + filetoRun)
    os.chdir("/home/fenics/shared/murtazo/navier_stokes_solver/results")
    result = ""
    with open  ("/home/fenics/shared/murtazo/navier_stokes_solver/results/drag_ligt.m", "r") as file:
        result = file.read()
    return (result, filetoRun)

def resultList(resulttupple):
    if not os.path.exists("/home/ubuntu/results"):
        os.makedirs("/home/ubuntu/results")
    #if os.file.exists("/home/ubuntu/results/" + resulttupple(2)) #Todo, använd det här innan vi gör mesh filerna
    with open("/home/ubuntu/results/" + resulttupple[1],"w+") as file:
        file.write(resulttupple[0])
if (__name__ == '__main__'):
    #meshmaker(one, two,three,four,five)
    #xmlConverter()
    #runAirfoil(filetoRun)
    resultList(("agagabaag","itworks"))