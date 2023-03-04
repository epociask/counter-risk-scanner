from src.clients.etherscan import (is_proxy, EtherscanAPI)
from src.clients.node import NodeAPI
from src.dep_graph import Graph

Contract = dict

derive_key = lambda source_key: source_key[source_key.rindex("/") + 1: len(source_key)]

class AssetRepresentation:


    def __init__(self, contract_dag: list[str] = []) -> None:
        self.sol_version: str = "0.8.0"
        self.is_proxy: bool = False
        ## All contracts in the asset representation DAG
        self.contract_dag: list[dict] = contract_dag

    def insert_contract(self, contract: Contract) -> None:
        self.contract_dag.append(contract)

    def get_head_proxy_contract(self) -> str:
        return self.contract_dag[0]

    def get_tail_delegate_contract(self) -> str:
        return self.contract_dag[-1]

    def __str__(self) -> str:
        return str(
            {
            "version": self.sol_version,
            "proxy": self.is_proxy,
            "contracts": self.contract_dag,
            })


class Builder:

    def __init__(self, explorer: EtherscanAPI, node: NodeAPI) -> None:
        self.explorer = explorer
        self.node = node

    @staticmethod
    def clean_version(version: str) -> str:
        if '+' in version:
            return version[1 : version.index('+')]
        
        return version[1 : len(version)-1]

    def build_asset_rep(self, address: str, contract_list: list[Contract]) -> AssetRepresentation:
        asset_rep: AssetRepresentation = AssetRepresentation(
            contract_dag=[
            {
                "address": address,
                "compiler_version": contract_list[0]["CompilerVersion"],
            }
        ])
        impl_address = None
        
        ## NOTE - you can DoS this tool by making bipartite calls between two contracts
        while True: ## Iterate over proxy...delegate call graph until no return

            append_value = {}
            proxy: bool = False
            for contract in contract_list:
                if is_proxy(contract):
                    print("Proxy detected")
                    proxy = True
                    impl_address: str = contract["Implementation"]
        
                    break

            if not proxy:
                break

            contract_list = self.explorer.get_contract_source(impl_address)
            asset_rep.contract_dag.append(
                    {
                "address": impl_address,
                "compiler_version": Builder.clean_version(contract_list[0]["CompilerVersion"]),
            })


        if len(contract_list) > 1:
            asset_rep.is_proxy = True

        return asset_rep

    def build_dependency_graph(self, compiled_contract: str, source_map: dict[str, dict[str, str]]) ->  Graph:
        print("Checking for contract ", compiled_contract)
        g: Graph = Graph(len(source_map.keys()))

        for source_i_key in source_map.keys():
            source_i_key = derive_key(source_i_key) if "/" in source_i_key else source_i_key

            for source_j_key, source_value in source_map.items():
                source_j_key = derive_key(source_j_key) if "/" in source_j_key else source_j_key


                if source_i_key == source_j_key:
                    continue
                
                if source_i_key in source_value["content"]:
                    g.add_ege(source_j_key, source_i_key)

                if f"contract {compiled_contract}" in source_value["content"]:
                    g.compiled_contract = source_j_key
                    print(g.compiled_contract)

        return g
