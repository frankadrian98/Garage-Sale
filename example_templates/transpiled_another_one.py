from simulation.simulation import *
from simulation.customer import *
from compilation.language.built_ins import *
m = Garage_Sale_Model(500, 6, 4)
print("Number of customers before")
print(m.no_customers)
print("")
print("Number of servers before")
print(m.no_servers)
print("")
m.add_customer()
m.add_customer()
m.remove_server(2)
m.sim()
print("Number of customers after")
print(m.no_customers)
print("")
print("Number of servers after")
print(m.no_servers)
print("")
print_sim_data(m, m.no_servers, m.no_cashiers)
index = 0
while ( index < l_len(m.servers) ):
    s = m.servers[index]
    print(s.id)
    index = (index + 1)