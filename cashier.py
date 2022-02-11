from agent import Agent
from customer import Customer
from collections import deque
from simulation import Garage_Sale_Model
 


class Cashier(Agent) :
    def __init__(self, id, model):
        self.busy = False
        self.actual_customer = None
        self.model = model
        self.cashier_queue =  deque([])
      
    def sim(self):
        if self.actual is None: 
            self.busy = True
            self.actual_customer =self.server_queue.pop()
            self.actual_customer._cservice = self.model.actual_sec  