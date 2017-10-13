from flask import Flask
from celery import Celery
import jsonExample


flaskCelery = Flask(__name__)
#app = Flask('flaskCelery')
flaskCelery.config['CELERY_BROKER_URL'] = 'pyamqp://'
flaskCelery.config['CELERY_RESULT_BACKEND'] = 'rpc://'

celery = Celery(flaskCelery.name, broker=flaskCelery.config['CELERY_BROKER_URL'], backend=flaskCelery.config['CELERY_RESULT_BACKEND'])
celery.conf.update(flaskCelery.config)

#task = my_background_task.delay()

@celery.task()
def myJsonCaller():
    # some long running task here
    return jsonExample.readJsonDataFile()



@flaskCelery.route('/', methods=['GET'])
def index():
    #flash('processing..\n')
    result = myJsonCaller.delay()
    if(result.ready()):
        return "true"
    else:
        return result.get(timeout=5000)
        
@flaskCelery.route('/hej/', methods=['GET'])
def index():
    return "hej back at u\n"
    

if __name__ == '__main__':
    
    flaskCelery.run(host='0.0.0.0',debug=True)
