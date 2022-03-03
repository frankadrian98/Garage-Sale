from logging import warning
import numpy as np


# Para saber la cantidad de clientes que han entrado a la tienda
def get_customers_arrived(model):
    customers_arrived = [
        customer.arrived for customer in model.customers]
    total_customers_arrived = np.sum(customers_arrived)
    return total_customers_arrived

# Para saber la cantidad de clientes que han sido atendidos por los servidores
def get_server_served(model):
    customers_server_served = [not(customer.service is None)
                        for customer in model.customers]
    customers_server_served = np.sum(customers_server_served)
    return customers_server_served

# Para saber la cantidad de clientes que han sido atendidos por los cajeros
def get_cashier_served(model):
    customers_cashier_served = [not(customer.cservice is None)
                        for customer in model.customers]
    customers_cashier_served = np.sum(customers_cashier_served)
    return customers_cashier_served

# Para saber la cantidad de clientes que se han perdido
def get_customers_lost(model):
    # customers_arrived = [
    #     customer._arrived for customer in model.customers]
    
    # customers_no_q = np.array([
    #     customer._q_entry is None for customer in model.customers])
    # no_customers_balked = np.sum(customers_arrived * customers_no_q)
    total_customers_lost = model. no_lost_customers
    return total_customers_lost

# Para saber la cantidad  promedio de clientes que hay en las colas de los servidores o de los cajeros
def avg_queue_size(model,queue):
    queue_size = [len(worker.queue) for worker in queue]
    avg_queue_size = np.mean(queue_size)
    return avg_queue_size


# Para saber el tiempo promedio de estancia en las colas de los clientes
def get_avg_waiting_time(model):
    server_queue_wait = [np.nan if customer.service is None else
                      customer.service - customer.qs_entry for customer in model.customers]
    cashier_queue_wait = [np.nan if customer.cservice is None else
                      customer.cservice - customer.qc_entry for customer in model.customers]
    
    avg_customer_wait = np.nanmean(server_queue_wait)
    return avg_customer_wait

def get_total_gain(model):
    return model.customer_value * get_cashier_served(model) - model.cost_workers * model.no_workers

  