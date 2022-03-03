from dis import dis
import matplotlib.pyplot as plt
from simulation import Garage_Sale_Model
import numpy as np
from Genetic_algorithm import MakeSim
# time = 3


    
# def split_workers(no_workers):
#     distributions = []
#     for i in range(1,no_workers):
#         distributions.append((i,no_workers-i))
#     return distributions
# def test(no_workers):
#     dist = split_workers(no_workers)
#     dist_dict = {}
#     for i in range(len(dist)):
#         mymodel = Garage_Sale_Model(no_servers =dist[i][0], no_cashiers = dist[i][1])
#         mymodel.sim()
#         dist_dict[(dist[i][0],dist[i][1])]= mymodel.collect_info
#         print(str(dist[i][0])+ ' servers ' +  str(dist[i][1]) + ' cashiers')
#         print('Customers Arrived ' + str(mymodel.collect_info['Customers Arrived' ][-1]))
#         print('Customers Server Served ' + str(mymodel.collect_info['Customers Server Served' ][-1]))
#         print('Customers Cashier Served ' + str(mymodel.collect_info['Customers Cashier Served' ][-1]))
#         print('Customers Lost ' + str(mymodel.collect_info['Customers Lost' ][-1]))
#         print('Average Server Queue Size ' + str(np.mean(mymodel.collect_info['Average Server Queue Size' ])))     
#         print('Average Casier Queue Size ' + str(np.mean(mymodel.collect_info['Average Cashier Queue Size' ])))  
#         print('Average Customer Wait ' + str(np.nanmean(mymodel.collect_info['Average Customer Wait'])))  
#         print('Total Gain '+ str(mymodel.collect_info['Total Gain' ][-1])) 
    

# test(10)
    
sim = MakeSim()     
sim.callgenetic(8)            
                    
