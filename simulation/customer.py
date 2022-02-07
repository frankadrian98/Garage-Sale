from .agent import Agent

class Customer(Agent):
    def __init__(self, unique_id, model):
        self._service_time = poisson(120).rvs()  # Tiempo en que lo va a atender los servidores
        self._entry_time = np.int(beta.rvs(1,5, size = 100) * time)  # Tiempo de entrada a la tienda 
        self._tolerance = poisson(60).rvs()  # Nivel de tolerancia del cliente
       
        #Valores para saber si el cliente esta o no en la tienda
        self._arrived = False
        self._exit = False    

        #Valores para saber si el cliente esta o no siendo atendido por un servidor
        self._service = None       
        self._service_exit = None
         
        #Valores para saber a que hora entro y salio el cliente al servicio
        self._timeserver_entry = None
        self._timeserver_exit = None
        
        #Para poder escoger el servidor que le va a atender
        def select_server(self):
         self._arrived = True
        #Si la cant de personas en la cola es mayor que el nivel de tolerancia del cliente
        # decira no entrar
         if len(customers_queue.queue) < self._tolerance:
            self.customers_queue.append(self)
            for i in range(len(server_array)): 
               if server_array[i].busy is False :
                self.timeserver_entry = self.model._current_time #Se evalua el tiempo de entrada al servidor
                server_array[i].actual= self   #Se annade al servidor el cliente
               

         else :
            self._exit = True 
       
        def pay_quickly(self):
         self._service_exit = self.model._current_time
