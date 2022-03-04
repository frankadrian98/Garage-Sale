from simulation.agent import Agent

#Clase padre de los trabajadores de la tienda
class Worker(Agent) :
    def __init__(self, id, model, service_time):
        super().__init__(id, model)
        self.busy = False          #Saber si esta ocupado o no
        self.actual_customer = None  #Saber cual es el cliente al cual esta atendiendo 
        self.service_time = service_time
        self.model = model            
        self.queue = []        #todos van a tener su respectiva cola
       
    def sim(self) -> None:
        pass