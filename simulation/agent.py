from simulation import Garage_Sale_Model
from random import Random

class Agent:

    def __init__(self, id: int, model : Garage_Sale_Model ) :
        self.id = id
        self.model = model
        
    def sim(self) -> None:
        pass

    def advance(self) -> None:
        pass

    