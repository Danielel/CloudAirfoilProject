from celery import Celery
import time


broker_url = 'amqp://acc9:aub1923lksad32@130.239.81.221:5672/acc9-host'
#app = Celery('celeryTesting', broker='pyamqp://guest@localhost//')
app = Celery('celeryTesting', backend='rpc://', broker=broker_url,  worker_prefetch_multiplier=1)
#app = Celery('celeryTesting', broker=broker_url)

@app.task
def add(x, y):
    time.sleep(5)
    return x + y
    
    #celery flower --broker=amqp://acc9:aub1923lksad32@130.239.81.221:5672/acc9-host//
@app.task
def doingSlowWork():
    time.sleep(10)
    return "HELLO!\n"