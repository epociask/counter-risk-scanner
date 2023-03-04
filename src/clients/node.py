from web3 import Web3
from dataclasses import dataclass

@dataclass
class GnosisState:
    m: int
    n: int
    score: float

class NodeAPI:
    def __init__(self, rpc_url: str, gnosis_abi: list[dict]) -> None:
        self.rpc_url = rpc_url
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))

        self.gnosis_abi = gnosis_abi

    def get_owner(self, address: str, contract_abi: list[dict]) -> str:
        contract = self.w3.eth.contract(address=address, abi=contract_abi)
        return contract.caller().owner()
    
    def get_gnosis_state(self, address: str) -> GnosisState:
        contract = self.w3.eth.contract(address=address, abi=self.gnosis_abi)

        m: int = int(contract.caller().getThreshold())
        n: int = int(contract.caller().getOwners())
        score: float = (m/n)

        return GnosisState(m, n, score)
