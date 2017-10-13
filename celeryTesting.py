from celery import Celery

broker_url = 'amqp://acc9:aub1923lksad32@130.239.81.221:5672/acc9-host'
#app = Celery('celeryTesting', broker='pyamqp://guest@localhost//')
app = Celery('celeryTesting', backend='amqp', broker=broker_url)

@app.task
def add(x, y):
    return x + y