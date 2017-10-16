from celery import Celery
import os


#broker_url = 'amqp://acc9:aub1923lksad32@130.239.81.221:5672/acc9-server'
broker_url = 'amqp://acc9:aub1923lksad32@192.168.1.42:5672/acc9-server'

#app = Celery('celeryTesting', broker='pyamqp://guest@localhost//')
app = Celery('WorkerTasks', backend='rpc://', broker=broker_url,  worker_prefetch_multiplier=1)
#app = Celery('celeryTesting', broker=broker_url)

@app.task
def add(x, y):
    return x + y
    
    #celery flower --broker=amqp://acc9:aub1923lksad32@130.239.81.221:5672/acc9-server/
@app.task
def runAirfoilOnWorker(wholeDamnXmlDict):
    return runAirfoilOnWorkerWithAirfoilArgs(wholeDamnXmlDict, 10, 0.0001, 10, 0.005)

#10 samples, run with the viscosity
#of nu=0.0001 and speed of v=10.0, total time is T=1
@app.task
def runAirfoilOnWorkerWithAirfoilArgs(wholeDamnXmlDict, samples, viscosity, speed, time):
    if not os.path.exists("/home/fenics/shared/receivedXML/"):
        os.makedirs("/home/fenics/shared/receivedXML/")
    os.chdir("/home/fenics/shared/receivedXML/")
    with open(wholeDamnXmlDict["filename"], "w+") as xmlFile:
        xmlFile.write(wholeDamnXmlDict["content"])
    airfoilText = "./airfoil " + str(samples) + " " + str(viscosity) + " " + str(speed) + " " + str(time) + " ./"
    os.system(airfoilText + wholeDamnXmlDict["filename"])
    os.chdir("/home/fenics/shared/murtazo/navier_stokes_solver/results")
    result = ""
    with open("/home/fenics/shared/murtazo/navier_stokes_solver/results/drag_ligt.m", "r") as file:
        result = file.read()
    return (result, wholeDamnXmlDict["filename"])
    
