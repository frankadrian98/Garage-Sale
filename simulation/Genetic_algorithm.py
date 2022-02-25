from random import Random
from simulation import Garage_Sale_Model



class Individual:
    def __init__(self) :
        self.Indcustomer = 0
        self.Indserver = 0
        self.Indcashier = 0
        self.random = Random

    def Random_individual(self):
        individual = Individual()
        individual.Indcustomer = self.random.randrange(1,100)
        individual.Indserver = self.random.randrange(2,5)
        individual.Indcashier = self.random.randrange(1,3)
        return individual

    def Individual_poblation(self):
        total = self.random.randrange(250)
        poblation = []
        for i in range(total):
            poblation.append(self.Random_individual())
        return poblation

    def Mutation(self):
        prop = self.random.randrange(0,2)
        if(prop == 0):
            self.Indcustomer = self.random.randrange(1,100, self.Indcustomer)
        elif(prop ==1):
            self.Indserver = self.random.randrange(2,5, self.Indserver)
        else:
            self.Indserver = self.random.randrange(1,3, self.Indcashier)