import subprocess
import os
one = int(input("What is the first parameter?/n"))
two = int(input("What is the second parameter?/n"))
three = int(input("What is the third parameter?/n"))
four = int(input("What is the fourth parameter?/n"))
five = int(input("What is the fifth parameter?/n"))

def meshmaker(one,two,three,four, five): #the five input variables
    q = subprocess.Popen(["cd /home/fenics/shared/murtazo/cloudnaca/"], stdout=subprocess.PIPE)
    p = subprocess.Popen(["/home/fenics/shared/murtazo/cloudnaca/runme.sh", one + " " + two + " " + three + " " + four + " " + five], stdout=subprocess.PIPE)

    print (p.communicate())


    
     #ToDO/ hitta sökväg till /home/fenics/shared/murtazo/cloudnaca# ./runme.sh
     #Så vi kan köra run me på inten
if (__name__ == '__main__'):
    meshmaker(one, two,three,four,five)
    #xmlConverter(one,two,three,four,five)
    #runAirfoil()
def xmlConverter():
    for fileName in os.listdir("/home/fenics/shared/murtazo/cloudnaca/msh/"):
        #Todo kom ihåg att kolla om vi behöver ta 
    q = subprocess.Popen(["dolfin-convert " +  "/home/fenics/shared/murtazo/cloudnaca/msh" + fileName  + " " + fileName + "xml"], stdout=subprocess.PIPE)

    print(q.communicate())

    def runAirfoil():
        r = subprocess.Popen(["/home/fenics/shared/murtazo/navier_stokes_solver# ./airfoil  10 0.0001 10. 1 ../cloudnaca/msh/ " + one + " " + two + " " + three +  " " + four + " " + five + "xml"], stdout=subprocess.PIPE)

        print(r.communicate())