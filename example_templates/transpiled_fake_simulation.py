actual_sec = 1
time = ((5 * 60) * 60)
no_customers = 100
no_servers = 5
no_cashiers = 2
def get_workers(no_s, no_c):
    return [no_s, no_c]
gw = get_workers(no_servers, no_cashiers)
no_servers = gw[0]
no_cashiers = gw[1]
if ( no_servers < no_cashiers ):
    print("Servers amount must be greater than cashiers, continue at your risk")
avg_line_time = 80
avg_service_time = 160
avg_cashier_time = 100
no_lost_costumers = 0
customers = []
index = 0
while ( index < no_customers ):
    customer = Customer(index)
    l_append(customers, customer)
    index = (index + 1)
servers = []
while ( index < no_servers ):
    server = Server(index)
    l_append(servers, server)
    index = (index + 1)
cashiers = []
index = 0
while ( index < no_cashiers ):
    cashier = Cashier(index)
    l_append(cashiers, cashier)
    index = (index + 1)
def sim():
    i = 0
    while ( i < l_len(customers) ):
        custom = customers[i]
        actual_sec = (actual_sec + 1)
        i = (i + 1)
sim()