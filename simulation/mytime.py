from collections import OrderedDict

from typing import Dict, Iterator, List, Optional, Union
from agent import Agent
from model import Model


TimeT = Union[float, int]


class BaseScheduler:

    def __init__(self, model: Model) -> None:
        self.model = model
        self.steps = 0
        self.time: TimeT = 0
        self._agents: Dict[int, Agent] = OrderedDict()

    def add(self, agent: Agent) -> None:
        if agent.id in self._agents:
            raise Exception(
                f"Agent with unique id {repr(agent.id)} already added to scheduler"
            )

        self._agents[agent.id] = agent

    def remove(self, agent: Agent) -> None:
        del self._agents[agent.id]

    def step(self) -> None:
        for agent in self.agent_buffer(shuffled=False):
            agent.step()
        self.steps += 1
        self.time += 1

    def get_agent_count(self) -> int:
        return len(self._agents.keys())

    @property
    def agents(self) -> List[Agent]:
        return list(self._agents.values())

    def agent_buffer(self, shuffled: bool = False) -> Iterator[Agent]:
        agent_keys = list(self._agents.keys())
        if shuffled:
            self.model.random.shuffle(agent_keys)

        for key in agent_keys:
            if key in self._agents:
                yield self._agents[key]


class RandomActivation(BaseScheduler):
    def step(self) -> None:
        for agent in self.agent_buffer(shuffled=True):
            agent.step()
        self.steps += 1
        self.time += 1


class SimultaneousActivation(BaseScheduler):

    def step(self) -> None:
        agent_keys = list(self._agents.keys())
        for agent_key in agent_keys:
            self._agents[agent_key].step()
        for agent_key in agent_keys:
            self._agents[agent_key].advance()
        self.steps += 1
        self.time += 1


class StagedActivation(BaseScheduler):

    def __init__(self,
        model: Model,
        stage_list: Optional[List[str]] = None,
        shuffle: bool = False,
        shuffle_between_stages: bool = False,
    ) -> None:
        super().__init__(model)
        self.stage_list = ["step"] if not stage_list else stage_list
        self.shuffle = shuffle
        self.shuffle_between_stages = shuffle_between_stages
        self.stage_time = 1 / len(self.stage_list)

    def step(self) -> None:
        agent_keys = list(self._agents.keys())
        if self.shuffle:
            self.model.random.shuffle(agent_keys)
        for stage in self.stage_list:
            for agent_key in agent_keys:
                getattr(self._agents[agent_key], stage)()  # Run stage
            if self.shuffle_between_stages:
                self.model.random.shuffle(agent_keys)
            self.time += self.stage_time

        self.steps += 1