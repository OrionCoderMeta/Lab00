from dataclasses import dataclass
from model.pilot import Pilot


@dataclass
class Arco:
    n1 : Pilot
    n2 : Pilot
    peso : float

    def __str__(self):
        return f"{self.n1.id} -> {self.n2.id} | weight = {self.peso}"