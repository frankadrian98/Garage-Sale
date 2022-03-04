from random import choice
import numpy as np
from simulation.simulation import Garage_Sale_Model
from simulation.check_metrics import get_total_gain
from simulation.behaviors import *



class Genetic_algorithm:
    def __init__(self) :
        self.behavior = [select_by_time,select_random,select_min]

    def Parents (self, individuals, Maximize):
        count = len(individuals)
        total = np.ceil(count * 0.6)
        maxi = []
        for i in range(len(individuals)):
            maxi.append(Maximize(individuals[i]))
        
        result = [i for _,i in sorted(zip(maxi,individuals), key = lambda x: x[0],reverse = True)]
        fittest = [result[i] for i in range(int(total))]

        return fittest
    
    def Children(self, parents, total_poblation):
        children = []
        for i in range(total_poblation):
            first = parents[random.randint(0, len(parents)-1)]
            second = parents[random.randint(0, len(parents)-1)]
            children.append(self.MakeChild(first,second))
        return children

    def MakeChild(self, first, second):
            child = Individual()
            prob = random.random()
            
            # Si la probabilidad es menor de 0.45 
            # insertar el gen del padre 1
            if prob < 0.45:
                child.no_customers = first.no_customers
                child.behavior = [self.behavior.index(f) for f in first.behavior]
                child.no_servers = second.no_servers
                child.no_cashiers = second.no_cashiers

             # Si la probabilidad esta entre  0.45 and 0.90 
            # insertar el gen del padre 2
            elif prob < 0.90:
                child.no_customers = second.no_customers
                child.behavior = [self.behavior.index(f) for f in second.behavior]
                child.no_servers = first.no_servers
                child.no_cashiers = first.no_cashiers
 
           #de lo contrario insertar el gen mutado
            else:
                for i in range(4):
                    r = random.randint(0,1)
                    if r:
                        child.no_customers = first.no_customers
                        child.behavior =  [self.behavior.index(f) for f in first.behavior]
                        child.no_servers = second.no_servers
                        child.no_cashiers = second.no_cashiers
                    else:
                        child.no_customers = second.no_customers
                        child.behavior = [self.behavior.index(f) for f in second.behavior]
                        child.no_servers = first.no_servers
                        child.no_cashiers = first.no_cashiers
                child.Mutation()
                
            return child

    def Run (self, individuals, Maximize):
        parents  = self.Parents(individuals, Maximize) # mejores padres
        children = self.Children(parents, len(individuals)) 
        individuals = []
        return children
 


class Individual:
    def __init__(self, no_customers = 0 , no_servers = 0, no_cashiers = 0, indbehavior = [] ) :
        self.no_customers = no_customers
        self.no_servers = no_servers
        self.no_cashiers = no_cashiers
        self.behavior = indbehavior   


    def Mutation(self):
        prob = random.randint(0,3)
        if prob == 0:
            self.no_customers = random.choice(list(set([x for x in range(1,501)])-set([self.no_customers])))
            self.behavior = [random.randint(0,MakeSim.default_behavior_count-1) for o in range(self.no_customers)] 
        elif prob==1:
            self.no_servers = random.choice(list(set([x for x in range(1,9)])-set([self.no_servers])))
        elif prob == 2:
            self.no_cashiers = random.choice(list(set([x for x in range(1,10-self.no_servers)])-set([self.no_cashiers])))
        else:
            self.behavior = [random.randint(0,MakeSim.default_behavior_count-1) for o in range(self.no_customers)] 
    
class MakeSim:
    default_behavior_count  = 3
    def __init__(self, behaviors=[select_by_time,select_random,select_min]):
        
        MakeSim.default_behavior_count =  len(behaviors)
        self.behaviors = behaviors
        

    def run( self,individual):
        beh=[]
        for i in range (individual.no_customers):
            beh.append(self.behaviors[individual.behavior[i]])

        mysimulation = Garage_Sale_Model( individual.no_customers, individual.no_servers, individual.no_cashiers, beh)
        mysimulation.sim()
        print(str(mysimulation.no_servers)+ ' servers ' +  str(mysimulation.no_cashiers) + ' cashiers')
        print('Customers Arrived ' + str(mysimulation.collect_info['Customers Arrived' ][-1]))
        print('Customers Server Served ' + str(mysimulation.collect_info['Customers Server Served' ][-1]))
        print('Customers Cashier Served ' + str(mysimulation.collect_info['Customers Cashier Served' ][-1]))
        print('Customers Lost ' + str(mysimulation.collect_info['Customers Lost' ][-1]))
        print('Average Server Queue Size ' + str(np.mean(mysimulation.collect_info['Average Server Queue Size' ])))     
        print('Average Casier Queue Size ' + str(np.mean(mysimulation.collect_info['Average Cashier Queue Size' ])))  
        print('Average Customer Wait ' + str(np.nanmean(mysimulation.collect_info['Average Customer Wait'])))  
        print('Total Gain '+ str(mysimulation.collect_info['Total Gain' ][-1])) 
        return mysimulation

    def Random_individual(self):
        individual = Individual()
        individual.no_customers = random.randint(1,500)
        individual.no_servers = random.randint(1,9)
        individual.no_cashiers = random.randint(1, 10 -individual.no_servers)
        individual.behavior = [random.randint(0, MakeSim.default_behavior_count-1) for o in range(individual.no_customers)]    
        return individual

    def Individual_poblation(self, countpoblation):
        poblation = []
        for i in range(countpoblation):
            poblation.append(self.Random_individual())
        return poblation

    def callgenetic(self, countpoblation, iterations = 5):
        mygenetic = Genetic_algorithm()
        poblation = self.Individual_poblation(countpoblation)
        for i in range(iterations):
            print('Generation '+str(i))
            executed = [self.run(p) for p  in poblation]
            poblation = mygenetic.Run(executed, get_total_gain)
        

        
            


