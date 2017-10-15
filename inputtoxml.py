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
            os.system("rm " + fileName)



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

@app.route('/')
#Todo (klientsidan) hur vi pratar med vår server för http://130.239.81.207:5000/post?id=1232  , man definerar varje parameter efter ? i sökvägen (post?)
def requesters():
    para1 = request.args.get('arg1') #ska ge parametrarna som vi skickar in till servern 
    para2 = request.args.get('arg2')
    para3 = request.args.get('arg3')
    para4 = request.args.get('arg4')
    para5 = request.args.get('arg5')
    if(true) #Todo finns uträkningarna för (para1,para2,para3,para4,para5), (vi behöver veta namn convention)
        return("already done these calculations") #can also return the results from the file in results in the main server
    else
        meshmaker(para1,para2,para3,para4,para5)
        xmlConverter(filetorun = "nameoffilewejustmade") #Todo här behöver vi naming convention som parameter i xml converter
        resultList = #runAirfoil(filetorun) #Todo skicka till Celery workers
        #se till att den väntar på svar från runAirfoil
        resultList(("vad som ska skrivas i resultatet, nr 0 i tuppel"),"nameoffilewejustmade.xml, nr 2 i tuppel resultlist") #todo, uppdatera resultList parametrar
