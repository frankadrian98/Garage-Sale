
from compilation.language.types import *
import numpy as np

def l_append(_list,elem):
    _list.append(elem)

def l_remove(_list,elem):
    _list.remove(elem)

def l_len(_list):
    return len(_list)

def randint(_from,_to):
    return random.randit(_from,_to)

def print_sim_data(mymodel,servers,cashiers):
    print(str(servers)+ ' servers ' +  str(cashiers) + ' cashiers')
    print('Customers Arrived ' + str(mymodel.collect_info['Customers Arrived' ][-1]))
    print('Customers Server Served ' + str(mymodel.collect_info['Customers Server Served' ][-1]))
    print('Customers Cashier Served ' + str(mymodel.collect_info['Customers Cashier Served' ][-1]))
    print('Customers Lost ' + str(mymodel.collect_info['Customers Lost' ][-1]))
    print('Average Server Queue Size ' + str(np.mean(mymodel.collect_info['Average Server Queue Size' ])))     
    print('Average Casier Queue Size ' + str(np.mean(mymodel.collect_info['Average Cashier Queue Size' ])))  
    print('Average Customer Wait ' + str(np.nanmean(mymodel.collect_info['Average Customer Wait'])))  
    print('Total Gain '+ str(mymodel.collect_info['Total Gain' ][-1])) 