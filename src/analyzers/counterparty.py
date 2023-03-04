from src.analyzers.abstract_analyzer import Analyzer
from src.utils import (abi_hash, sha256_hash)

class CounterPartyAnalyzer(Analyzer):
    def __init__(self, node_api,
                 gnosis_abi: list[dict], ownable_abi: list[dict]) -> None:
        self.gnosis_fingerprint: hex = abi_hash(gnosis_abi)
        self.ownable_abi = ownable_abi

    def assess(address: str):
        pass
    
    def risk_score():
        pass

    def is_gnosis_multisig(self, contract_abi: list[dict]) -> bool:
        finger_print: str = abi_hash(contract_abi)

        return finger_print == self.gnosis_fingerprint

    def has_owner(self, contract_abi: dict) -> bool:
        ownable_len: int = len(self.ownable_abi)
        overlap_count: int = 0

        # O(n^2) is not ideal
        # TODO - See if there's anyway to reduce this
        for ownable_item in self.ownable_abi:
            for arbitrary_item in contract_abi:
                if ownable_item == arbitrary_item:
                    overlap_count += 1

        return (ownable_len) == overlap_count


