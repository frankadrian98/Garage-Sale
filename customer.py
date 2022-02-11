from agent import Agent
from server import Server
from cashier import Cashier
from simulation import Garage_Sale_Model
from scipy.stats import poisson
from simulation import no_lost_customers 
import numpy as np

time = 10800

class Customer(Agent):
    def __init__(self, id, model):
        self.id = id
        self._service_time = poisson(120).rvs()  # Tiempo en que lo va a atender los servidores
        self._entry_time = poisson(180).rvs() * self.model.actual_sec  # Tiempo de entrada del cliente a la tienda 
        self._tolerance = 5  # Nivel de tolerancia del cliente
        self._cashier_time = poisson(60).rvs()  # Tiempo en que lo va a atender el cajero
       
        #Valores para saber si el cliente esta o no en la tienda
        self._arrived = False
        self._exit = False   

         #Valor para saber cuando el cliente entra de la cola para los servidores
        self._qs_entry = None
       # self._qs_exit = None
          
         #Valor para saber a que hora el cliente  entra al servidor
        self._service = None       
        # self._service_exit = None
         
         #Valor para saber cuando entro y salio de la cola para los cajeros
        self._qc_entry = None
        # self._qc_exit = None

         #Valor para saber a que hora el cliente  entra y sale del cajero
        self._cservice = None       
        self._cservice_exit = None
        
        #Para poder escoger el servidor que le va a atender
        def select_server(self):
          self._arrived = True
           #Si la cant de personas en la cola x es mayor que el nivel de tolerancia del cliente
           # decidira no ponerse en esa cola
          for i in range(len(self.model.servers)):
           if len(Server.server_queue.queue) < self._tolerance:
            self.server_queue.append(self) #Se annade el cliente a la cola del servidor
            self._qs_entry = model.actual_sec   #Se actualiza el tiempo de entrada a la cola
          self._exit = True   #Si no encuentra una cola que cumple sus requisitos se va del sistema
          
        def select_cashier(self):
            #Si la cant de personas en la cola x es mayor que el nivel de tolerancia del cliente
            # decidira no ponerse en esa cola
          for i in range(len(self.model.cashiers)):
            if len(Cashier.cashier_queue.queue) < self._tolerance:
             self.cashier_queue.append(self) #Se annade el cliente a la cola del cajero
             self._qc_entry = self.model.actual_sec  #Se actualiza el tiempo de entrada a la cola
          self._exit = True #Si no encuentra una cola que cumple sus requisitos se va del sistema
          
        def step(self) :
            if (self._arrived == False) or (self.model.actual_sec >= self.entry_time):
              self.select_server()
             
    
       
       
