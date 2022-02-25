
from agent import Agent
from scipy.stats import poisson
import numpy as np

time = 10800

class Customer(Agent):
    def __init__(self, id, model):
        self.id = id
        self.model = model
        self.line_time = poisson(80).rvs()
        self._service_time = poisson(160).rvs()  # Tiempo en que lo va a atender los servidores
        self._entry_time = poisson(120).rvs() + self.model.entry  # Tiempo de entrada del cliente a la tienda 
        self.model.entry = self._entry_time
        self._tolerance = 5  # Nivel de tolerancia del cliente
        self._cashier_time = poisson(100).rvs()  # Tiempo en que lo va a atender el cajero
       
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
          self.minserver = np.argmin([len(server.queue) for server in self.model.servers])
          self.chosens = self.model.server[self.minserver]
           #Si la cant de personas en la cola x es mayor que el nivel de tolerancia del cliente
           #decidira no ponerse en esa cola
          if len(self.chosens) < self._tolerance:
              self.chosens.queue.append(self) #Se annade el cliente a la cola del servidor
              self._qs_entry = self.model.actual_sec   #Se actualiza el tiempo de entrada a la cola
          else:
            self._exit = True   #Si no encuentra una cola que cumple sus requisitos se va del sistema
          
        def select_cashier(self):
          self.mincashier = np.argmin([len(cashier.queue) for cashier in self.model.cashiers])
          self.chosenc = self.model.cashier[self.mincashier]
           #Si la cant de personas en la cola x es mayor que el nivel de tolerancia del cliente
           #decidira no ponerse en esa cola
          if len(self.chosenc) < self._tolerance:
              self.chosenc.queue.append(self) #Se annade el cliente a la cola del cajero
              self._qc_entry = self.model.actual_sec #Se actualiza el tiempo de entrada a la cola
          else:
           self._exit = True #Si no encuentra una cola que cumple sus requisitos se va del sistema

        def out_server(self):
          self._qc_entry = self.model.actual_sec
          self.chosens.actual_customer = None

        def pay(self):
          self._cservice_exit = self.model.actual_sec
          self.chosenc.actual_customer = None  
        


        def sim(self) :
            if (self._arrived == False) & (self.model.actual_sec >= self.entry_time):
              self.select_server()
            elif(self._qs_entry != None):
              if(self.model.actual_sec - self._qs_entry ==  self.line_time):
                 self.chosens.sim()
            elif (self._service != None):
              if(self.model.actual_sec - self._service ==  self._service_time):
                out_server()
                select_cashier()
            elif(self._qc_entry != None):
              if(self.model.actual_sec - self._qc_entry ==  self.line_time):
                 self.chosenc.sim()
            elif(self._cservice != None):
              if(self.model.actual_sec - self._cservice ==  self._cashier_time):
                 pay()


       
       


