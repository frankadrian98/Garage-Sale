
from worker import Worker


class Cashier(Worker) :
    def __init__(self, id, model,service_time):
        super().__init__(id, model,service_time)
       
       
      
    def sim(self):
        if self.actual_customer is None and self.queue: 
            self.busy = True
            self.actual_customer =self.queue.pop(0)
            self.actual_customer.cservice = self.model.actual_sec
  