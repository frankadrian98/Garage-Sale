from agent import Agent




class Server(Agent) :
    def __init__(self, id, model):
        self.busy = False
        self.actual_customer = None
        self.model = model
        self.queue = []
      
    def sim(self):
        if self.actual_customer is None: 
            self.busy = True
            self.actual_customer = self.server_queue.pop(0)          
            self.actual_customer._service = self.model.actual_sec
           
            
             