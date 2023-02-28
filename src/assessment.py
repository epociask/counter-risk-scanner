from dataclasses import dataclass
from enum import Enum

class Risk(Enum):
    counter_party = "Counterparty Risk"
    market = "Market Risk"

class CounterParty(Risk):
    centralized_superuser = ""
    custodial_access = ""

@dataclass
class Risk:
    name: str
    score: int # TODO - Map to some enum
    description: str
    id: str

class Assessment():

    def __init__(self) -> None:
        self.risks: list[Risk] = []

    def get_trust_score(self):
        pass

    def get_permission_risk(self):
        pass

class CounterPartyAssessment(Assessment):
    pass

class MarketAssessment(Assessment):
    pass