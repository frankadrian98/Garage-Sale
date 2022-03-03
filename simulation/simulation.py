from behaviors import *
from logging import raiseExceptions
from scipy.stats import poisson
from agent import Agent
from customer import Customer
from server import Server
from cashier import Cashier
from check_metrics import *
from random_events import event_selector
import random


class Garage_Sale_Model:
    def __init__(self,no_customers = 500, no_servers = 5, no_cashiers = 5 , behavior = [], cost_workers = 200, customer_value = 10,time = 7200):
        self.actual_sec = 1 # segundo actual por el que va la simulacion
        self.time = time   #simularemos las acciones de la tienda por 3 horas (10800 seg)
        self.no_customers = no_customers  # cant de clientes que entraran en las horas determinadas
        self.no_servers = no_servers #cant de servidores que tiene la tienda
        self.no_cashiers = no_cashiers #cant de cajeros que tiene la tienda
        self.cost_workers = cost_workers #costo de cada trabajador
        self.customer_value = customer_value # dinero bruto ganado por cada cliente
        self.behavior = behavior + [ select_by_time, select_random , select_min] #lista de los comportamientos de los clientes
       
        # self.avg_line_time = 80 # cant de tiempo promedio qu se demora un cliente en la cola
        # self.avg_service_time = 160 # cant de tiempo promedio el cual se demora un servidor en atender al cliente
        # self.avg_cashier_time = 100  # cant de tiempo promedio el cual se demora un cajero en atender al cliente
        self.no_lost_customers = 0 #cant de clientes que se fueron sin servicio
        self.entry = 1


        #Creando los agentes
        #Creando los clientes
        self.customers = [] #Crear los clientes que van a estar en la simulacion
        for i in range(self.no_customers) :
            
            customer = Customer(i, self, self.behavior[random.randint(0,len(self.behavior) - 1)])
            
             #asignar funcion rndom de la lista de funciones
            self.customers.append(customer)
        #Creando los servidores
        self.servers = [] # Crear los servidores de la simulacion
        for i in range(self.no_servers) :
            server = Server(i, self, poisson(160).rvs()  )
            self.servers.append(server)
        #Creando los cajeros
        self.cashiers = [] #Crear los cajeros de la simulacion
        for i in range(self.no_cashiers):
            cashier = Cashier(i, self,  poisson(100).rvs() )
            self.cashiers.append(cashier)
        self.totalagent = self.customers + self.servers + self.cashiers

        self.collect_info = {'Customers Arrived' : [],
                        'Customers Server Served' : [] ,                   
                        'Customers Cashier Served' : [],
                        'Customers Lost': [],
                        'Average Server Queue Size': [],
                        'Average Cashier Queue Size': [],
                        'Average Customer Wait':[],
                        'Total Gain': []
        }

        event_selector(self)

    def add_customer (self, behavior):
        index = self.no_customers
        agg_customer = Customer(index, self, behavior)
        self.customers.append(agg_customer)
        self.no_customers += 1
        self.totalagent +=1
    
    def remove_customer(self, id=-1):
        self.customers.pop(id)
        self.no_customers -= 1
        self.totalagent -= 1

    def add_server(self):
        agg_server = Server(self.no_servers, self) 
        self.servers.append(agg_server)
        self.no_servers += 1
        self.totalagent +=1
    
    def remove_server(self, id=-1):
        self.servers.pop(-1)
        self.no_servers -= 1
        self.totalagent -= 1

    def add_cashier(self):
        agg_cashier = Cashier(self.no_cashiers , self) 
        self.servers.append(agg_cashier)
        self.no_cashiers += 1
        self.totalagent +=1
    
    def remove_cashier(self, id=-1):
        self.cashiers.pop(-1)
        self.no_cashiers -= 1
        self.totalagent -= 1

    def add_behavior(self, agg_behavior):
        self.behavior.append(agg_behavior)

     
    def update_data(self):
        self.collect_info['Customers Arrived'].append(get_customers_arrived(self))
        self.collect_info['Customers Server Served'].append(get_server_served(self))
        self.collect_info['Customers Cashier Served'].append(get_cashier_served(self))
        self.collect_info['Customers Lost'].append(get_customers_lost(self))
        self.collect_info['Average Server Queue Size'].append(avg_queue_size(self, self.servers))
        self.collect_info['Average Cashier Queue Size'].append(avg_queue_size(self, self.cashiers))
        self.collect_info['Average Customer Wait'].append(get_avg_waiting_time(self))
        self.collect_info[ 'Total Gain'].append(get_total_gain(self))
      
     

        
       

    

   
    def sim(self):
        while self.actual_sec != self.time:
            self.update_data()
            for agent in self.totalagent:
                agent.sim()
            self.actual_sec += 1