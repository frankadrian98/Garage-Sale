from .agent import Agent

class Server(Agent) :
    def __init__(self, unique_id, model):
        self.busy = False
        self.actual = None 
        self.actual._service = self.model._current_time
      

    def sim(self):
        if self.actual is None: 
             self.actual._service_exit = self.model._current_time - 1