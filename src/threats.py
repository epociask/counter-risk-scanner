from dataclasses import dataclass
from enum import Enum

@dataclass
class Threat:
    name: str
    description: str
    risk: str

class Assessment():

    def __init__(self, r, c ) -> None:
        self.risky_counterparty: str  = r 
        self.custodial_functions: list = c
        self.threats: list = []


    def get_trust_score(self):
        pass

    def get_permission_risk(self):
        pass

    def serialize(self):
        return {"counterparties": [self.risky_counterparty],
                "impacted_custodial_functions": self.custodial_functions,
                "threats": self.threats}
