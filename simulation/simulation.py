
from scipy.stats import poisson
from customer import Customer
from server import Server
from cashier import Cashier
import random


class Garage_Sale_Model:
  def __init__(self, no_servers, no_cashiers):
      self.actual_sec = 1 # segundo actual por el que va la simulacion
      self.time = 10800   #simularemos las acciones de la tienda por 3 horas (10800 seg)
      self.no_customers = 5  # cant de clientes que entraran en las horas determinadas
      self.no_servers = no_servers #cant de servidores que tiene la tienda
      self.no_cashiers = no_cashiers #cant de cajeros que tiene la tienda
      if(self.no_servers< self.no_cashiers):
          print ("La cantidad de servidores no pueden ser menor que la cantidad de cajeros")
         
      self.avg_line_time = 80 # cant de tiempo promedio qu se demora un cliente en la cola
      self.avg_service_time = 160 # cant de tiempo promedio el cual se demora un servidor en atender al cliente
      self.avg_cashier_time = 100  # cant de tiempo promedio el cual se demora un cajero en atender al cliente
      self.no_lost_customers = 0 #cant de clientes que se fueron sin servicio
      self.entry = 1
      #Creando los agentes
      self.customers = [] #Crear los clientes que van a estar en la simulacion
      for i in range(self.no_customers) :
          customer = Customer(i, self)
          self.customers.append(customer)
      self.servers = [] # Crear los servidores de la simulacion
      for i in range(self.no_servers) :
          server = Server(i, self)
          self.servers.append(server)
      self.cashiers = [] #Crear los cajeros de la simulacion
      for i in range(self.no_cashiers) :
        cashier = Cashier(i, self)
        self.cashiers.append(cashier)
   
  def sim(self):
      for custom in self.customers:
        custom.sim()
        self.actual_sec += 1
      



          
