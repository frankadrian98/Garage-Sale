import numpy as np
from scipy.stats import poisson
from scipy.stats import beta
from .time import RandomActivation
from .model import Model
import random

from typing import Any, Optional

# Tiempo total de la simulacion
time = 10800   #simularemos las acciones de la tienda por 3 horas (10800 seg)
no_customers = 100 # cant de clientes que entraran en las horas determinadas
no_servers = 4 #cant de servidores que tiene la tienda
server_array = [] #Array para saber si los servidores estan ocupados
avg_line_time = 120 # cant de tiempo promedio qu se demora un cliente en la cola
avg_service_time = 80 # cant de tiempo promedio el cual se demora un servidor en atender al cliente
customers_queue = [] #cant de clientes que hay en la cola para entrar a la tienda

        
       

class MyQueue(Model):
 def __init__(self, no_servers, no_customers, time ):
    self.schedule = RandomActivation(self)
    self._current_time = 1
    self.time = time
    self.no_customers = no_customers
    self.no_servers = no_servers
     
    self.customers = []
    self.server_array = []

    for i in range(self.no_customers):
        customer = Customer(i, self)
        self.schedule.add(customer)
        self.customers.append(customer)

    for i in range(self.no_servers):
        server = Server(i + no_customers , self)
        self.schedule.add(server)
        self.server_array.append(server)
   
            
 def sim(self):
    self._current_time += 1
    self.schedule.step()

          
