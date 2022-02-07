from .model import Model

class Agent:

    def __init__(self, id: int, model: Model) -> None:
        self.id = id
        self.model = model
        self.pos = None

    def step(self) -> None:
        pass

    def advance(self) -> None:
        pass

    @property
    def random(self) -> Random:
        return self.model.random