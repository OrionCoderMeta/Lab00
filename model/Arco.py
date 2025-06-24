from dataclasses import dataclass
from model.driver import Driver


@dataclass
class Arco:
    n1 : Driver
    n2 : Driver
    peso : float

    def __str__(self):
        return f"{self.n1.driverID} -> {self.n2.driverID} | weight = {self.peso}"