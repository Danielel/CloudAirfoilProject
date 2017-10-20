import os
import time
import subprocess
import sys
from subprocess import PIPE, run
import WorkerTasks
import createWorkers
import signal

minimum_workers = 1
max_workers = int(sys.argv[1])

def busyWorkers():
    busyWorkers = 0
    activeNow = WorkerTasks.app.control.inspect().active()
    if activeNow:
        for worker in activeNow:
             if activeNow[worker] != []:
                busyWorkers += 1
    return busyWorkers

def tasksInQueue():
    celery_queues = subprocess.check_output(['sudo','rabbitmqctl','list_queues', '-p', 'acc9-server']).decode('utf-8').split('\n')
    for line in celery_queues:
        if 'celery\t' in line:
            in_queue = int(line.split('\t')[1])
            break
    return in_queue


def signal_handler(signal, frame):
    print('\nYou pressed Ctrl+C! Killing worker')
    for worker in worker_array:
        createWorkers.killWorker(worker[1], worker[2])
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

currentActive = WorkerTasks.app.control.inspect().active()
if currentActive:
    current_workers = len(currentActive)
    print("This program needs to create the instances")
    exit()
else:
    current_workers = 0
worker_array = []
currentWorkerId = 0
while(True):
    while(current_workers < minimum_workers):
        print("Creating a worker to meet minimum workers")
        current_workers += 1
        currentWorkerId += 1
        (inst_id, vol_id) = createWorkers.createWorker("acc9-worker" + str(current_workers))
        worker_array.append(("acc9-worker" + str(current_workers), inst_id, vol_id))
    
    in_queue = tasksInQueue()
    print("Tasks in queue: " + str(in_queue))
    print("Current workers = " + str(current_workers))
    print("Busy workers = " + str(busyWorkers()))
        
    if current_workers < in_queue-1:
        while(current_workers < in_queue-1 and current_workers < max_workers):
            print("Creating another worker due to work in queue")
            current_workers += 1
            currentWorkerId += 1
            (inst_id, vol_id) = createWorkers.createWorker("acc9-worker" + str(current_workers))
            worker_array.append(("acc9-worker" + str(current_workers), inst_id, vol_id))
            in_queue = tasksInQueue()
        in_queue = tasksInQueue()
    
    
    if current_workers > in_queue+1 and current_workers > minimum_workers:
        currentActive = WorkerTasks.app.control.inspect().active()
        for worker in worker_array: 
            if currentActive['celery@c_' + str(worker[0])] == []:
                print("Killing a worker due to lack of work in queue")
                current_workers -= 1
                createWorkers.killWorker(worker[1], worker[2])
                worker_array.remove(worker)
                break
    print("")
    time.sleep(20) #takes quite a bit of time to do requests