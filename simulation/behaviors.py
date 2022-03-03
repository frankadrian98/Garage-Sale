import numpy as np 
import random

def select_by_time(queue):
  min_worker_id = np.argmin([worker.service_time for worker in queue]) 
  return queue[min_worker_id]


def select_random(queue):
    i = random.randint(0,len(queue)-1)
    return queue[i]
    

def select_min(queue):
  min_worker_id = np.argmin([len(worker.queue) for worker in queue]) 
  return queue[min_worker_id]

