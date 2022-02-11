
from scipy.stats import poisson
from customer import Customer
from server import Server
from cashier import Cashier
import random

class Garage_Sale_Model:
  def __init__(self):
    def __init__(self, no_customers = 100, no_servers = 4, no_cashiers = 2):
      self.actual_seg = 1 # segundo actual por el que va la simulacion
      self.time = 10800   #simularemos las acciones de la tienda por 3 horas (10800 seg)
      self.no_customers = no_customers  # cant de clientes que entraran en las horas determinadas
      self.no_servers = no_servers #cant de servidores que tiene la tienda
      self.no_cashiers = no_cashiers #cant de cajeros que tiene la tienda
      self.avg_line_time = 80 # cant de tiempo promedio qu se demora un cliente en la cola
      self.avg_service_time = 120 # cant de tiempo promedio el cual se demora un servidor en atender al cliente
      self.avg_cashier_time = 80  # cant de tiempo promedio el cual se demora un cajero en atender al cliente
      self.no_lost_customers = 0 #cant de clientes que se fueron sin servicio
      #Creando los agentes
      self.customers = [] #Crear los clientes que van a estar en la simulacion
      for i in range(self.no_customers) :
          customer = Customer(self, i)
          self.customers.append(customer)
      self.servers = [] # Crear los servidores de la simulacion
      for i in range(self.no_servers) :
          server = Server(self, i)
          self.servers.append(server)
      self.cashiers = [] #Crear los cajeros de la simulacion
      for i in range(self.no_cashiers) :
          cashier = Cashier(self, i)
          self.cashiers.append(cashier)
   
    def sim(self):
        self.actual_seg += 1



          
