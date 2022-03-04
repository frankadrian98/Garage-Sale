from simulation.agent import Agent
from scipy.stats import poisson , beta
from simulation.behaviors import *
import numpy as np

time = 10800

class Customer(Agent):
    def __init__(self, id, model, behavior):
        super().__init__(id, model)
       # self.id = id
       # self.model = model
        self.behavior = behavior
        self.entry_time  = np.int(beta(3, 3).rvs() * model.time) + 1
      #  self.entry_time = poisson(120).rvs() + self.model.entry  # Tiempo de entrada del cliente a la tienda 
        self.model.entry = self.entry_time
        self.line_time = poisson(80).rvs()  #Tiempo que va a esperar en las colas
        
        self.tolerance = poisson(5).rvs()  # Nivel de tolerancia del cliente
        
       
        #Valores para saber si el cliente esta o no en la tienda
        self.arrived = False
        self.exit = False   

         #Valor para saber cuando el cliente entra de la cola para los servidores
        self.qs_entry = None
       # self.qs_exit = None
          
         #Valor para saber a que hora el cliente  entra al servidor
        self.service = None       
        # self.service_exit = None
         
         #Valor para saber cuando entro y salio de la cola para los cajeros
        self.qc_entry = None
        # self.qc_exit = None

         #Valor para saber a que hora el cliente  entra y sale del cajero
        self.cservice = None       
        self.cservice_exit = None
        
        #Para poder escoger el servidor que le va a atender
    def select_server(self):
          self.arrived = True
          self.chosens = self.behavior(self.model.servers)
           #Si la cant de personas en la cola x es mayor que el nivel de tolerancia del cliente
           #decidira no ponerse en esa cola
          if len(self.chosens.queue) < self.tolerance:
              self.chosens.queue.append(self) #Se annade el cliente a la cola del servidor
              self.qs_entry = self.model.actual_sec   #Se actualiza el tiempo de entrada a la cola
          else:
            self.exit = True
            self.model.no_lost_customers +=1   #Si no encuentra una cola que cumple sus requisitos se va del sistema
          
    def select_cashier(self): 
          
          self.chosenc = self.behavior(self.model.cashiers)
           #Si la cant de personas en la cola x es mayor que el nivel de tolerancia del cliente
           #decidira no ponerse en esa cola
          if len(self.chosenc.queue) < self.tolerance:
              self.chosenc.queue.append(self) #Se annade el cliente a la cola del cajero
              self.qc_entry = self.model.actual_sec #Se actualiza el tiempo de entrada a la cola
          else:
           self.exit = True #Si no encuentra una cola que cumple sus requisitos se va del sistema
           self.model.no_lost_customers +=1 

    def out_server(self):
          self.qc_entry = self.model.actual_sec
          self.chosens.actual_customer = None

    def pay(self):
          self.cservice_exit = self.model.actual_sec
          self.chosenc.actual_customer = None  
        


    def sim(self) :
        if self.arrived == False and self.model.actual_sec >= self.entry_time:
            self.select_server()
       # elif self.qs_entry != None and self.model.actual_sec - self.qs_entry ==  self.line_time :
        elif self.service != None and self.model.actual_sec - self.service ==  self.chosens.service_time :
            self.out_server()
            self.select_cashier()
            self.chosens.sim()
       # elif self.qc_entry != None and self.model.actual_sec - self.qc_entry ==  self.line_time :
        elif self.cservice != None and self.model.actual_sec - self.cservice ==  self.chosenc.service_time :
            self.pay()
            self.chosenc.sim()


       


