from agent import Agent


class Server(Agent) :
    def __init__(self, unique_id,customer = None):
        super().__init__(unique_id,customer)
        self.busy = False
        self.actual = customer
        if customer:
            self.actual._service = self.model._current_time
      


    def sim(self):
        if self.actual is None: 
             self.actual._service_exit = self.model._current_time - 1