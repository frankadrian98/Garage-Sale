from simulation.simulation import *
from simulation.customer import *
from compilation.language.built_ins import *
from simulation.Genetic_algorithm import MakeSim
def split_workers(no_workers):
    distributions = []
    i = 1
    while ( i < no_workers ):
        l_append(distributions, i)
        l_append(distributions, (no_workers - i))
        i = (i + 1)
    return distributions
def test(workers):
    dist = split_workers(workers)
    i = 0
    best = Garage_Sale_Model(500, 1, (workers - 1))
    while ( i < l_len(dist) ):
        mymodel = Garage_Sale_Model(500, dist[i], dist[(i + 1)])
        x = mymodel.sim()
        print_sim_data(mymodel, dist[i], dist[(i + 1)])
        i = (i + 2)
        if (mymodel.get_total_gain() > best.get_total_gain()):
            best = mymodel
    print("******************************************")
    print("The best distributions for the workers was:")
    print_sim_data(best, best.no_servers, best.no_cashiers)
test(10)