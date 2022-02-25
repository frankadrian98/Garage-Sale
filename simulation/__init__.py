from simulation import Garage_Sale_Model

time = 10800
mymodel = Garage_Sale_Model(4,3)

for i in range(time):
    mymodel.sim()