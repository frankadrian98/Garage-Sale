from random import Random
import numpy as np
from simulation import Garage_Sale_Model
from check_metrics import get_total_profit



class Genetic_algorithm:
    def __init__(self) :
        self.random=Random

    def Parents (self, individuals, Maximize):
        count = len(individuals)
        total = np.ceil(count * 0.6)
        maxi = []
        for i in range(len(individuals)):
            maxi.append(Maximize(individuals[i]))
        
        result = [i for _,i in sorted(zip(maxi,individuals))]
        fittest = [result[i] for i in range(total)]

        return fittest
    
    def Children(self, parents):
        children = []
        for i in range( len(parents)/2):
            first = parents[self.random.randrange(0, len(parents-1))]
            second = parents[self.random.randrange(0, len(parents-1))]
            
            children.append(self.Makechild(first,second))
        return children

    def MakeChild(self, first, second):
            child = Individual()
        
            prob = self.random.random()

            # Si la probabilidad es menor de 0.45 
            # insertar el gen del padre 1
            if prob < 0.45:
                child.indcustomer = first.customer
                child.behavior = first.behavior
                child.indserver = second.server
                child.indcashier = second.indcashier

             # Si la probabilidad esta entre  0.45 and 0.90 
            # insertar el gen del padre 2
            elif prob < 0.90:
                child.indcustomer = second.customer
                child.behavior = second.behavior
                child.indserver = first.server
                child.indcashier = first.indcashier
 
           #de lo contrario insertar el gen mutado
            else:
                for i in range(4):
                    r = self.random.randrange(0,1)
                    if r:
                        child.indcustomer = first.customer
                        child.behavior = first.behavior
                        child.indserver = second.server
                        child.indcashier = second.indcashier
                    else:
                        child.indcustomer = second.customer
                        child.behavior = second.behavior
                        child.indserver = first.server
                        child.indcashier = first.indcashier
                child.Mutation()
                
            return child

    def Run (self, individuals, Maximize):
        parents  = self.Parents(individuals, Maximize) # mejores padres
        children = self.Children(parents) 
        individuals.Clear()
        individuals = children
        return individuals
 


class Individual:
    def __init__(self, indcustomer = 0 , indserver = 0, indcashier = 0, indbehavior = [] ) :
        self.indcustomer = indcustomer
        self.indserver = indserver
        self.indcashier = indcashier
        self.behavior = indbehavior
        self.random = Random

    

    

    def Mutation(self):
        prob = self.random.randrange(0,3)
        if prob == 0:
            self.indcustomer = self.random.randrange(1,500,self.indcustomer)
        elif prob==1:
            self.indserver = self.random.randrange(1,9,self.indserver)
        elif prob == 2:
            self.indcashier = self.random.randrange(1,9,self.indcashier)
        else:
            self.behavior = [self.random.randrange(0,MakeSim.default_behavior_count) for o in range(self.indcustomer)] 
    
class MakeSim:
    default_behavior_count  = 3
    def __init__(self, behaviors):
        if behaviors:
            MakeSim.default_behavior_count = len(behaviors)
        else:
            MakeSim.default_behavior_count = 3
        self.behaviors = behaviors
        self.random = Random
        

    def run( self,individual):
        beh=[]
        for i in range (individual.indcustomer):
            beh.append(self.behaviors[individual.behavior[i]])

        mysimulation = Garage_Sale_Model( individual.indcustomer, individual.indserver, individual.indcashier,beh)

        mysimulation.sim()

    def Random_individual(self):
        individual = Individual()
        individual.indcustomer = self.random.randrange(1,500)
        individual.indserver = self.random.randrange(1,9)
        individual.indcashier = self.random.randrange(1,9)
        individual.behavior = [self.random.randrange(0,len(self.behaviors)) for o in range(individual.indcustomer)]    
        return individual

    def Individual_poblation(self, countpoblation):
        total = self.random.randrange(countpoblation)
        poblation = []
        for i in range(total):
            poblation.append(self.Random_individual())
        return poblation

    def callgenetic(self, countpoblation):
        mygenetic = Genetic_algorithm()
        poblation = mygenetic.Run(self.Individual_poblation(countpoblation), get_total_profit)
        for i  in range(poblation):
            self.run(poblation)


