class Model:

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        cls._seed = kwargs.get("seed", None)
        cls.random = random.Random(cls._seed)
        return object.__new__(cls)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.running = True
        self.schedule = None
        self.current_id = 0

    def run_model(self) -> None:
        while self.running:
            self.step()

    def step(self) -> None:
        pass

    def next_id(self) -> int:
        self.current_id += 1
        return self.current_id

    def reset_randomizer(self, seed: Optional[int] = None) -> None:
        if seed is None:
            seed = self._seed
        self.random.seed(seed)
        self._seed = seed