from src.settings import (ETHERSCAN_API_KEY, ETHEREUM_RPC_ENDPOINT)
from src.settings import Network
from src.clients.etherscan import EtherscanAPI
from src.clients.node import (NodeAPI, GnosisState)

from src.analyzers.counterparty import CounterPartyAnalyzer
from src.system import SystemAPI
from src.threats import Assessment, Threat
import src.asset as asset
import json

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/assess', methods=['GET'])
def risk_assess():
    network: str = request.args.get("network")
    address: str = request.args.get("address")

    system: SystemAPI = SystemAPI()

    gnosis_abi: list[dict] = system.read_json_from_file("abi/gnosis_multisig.json")
    ownable_abi: list[dict] = system.read_json_from_file("abi/ownable.json")

    explorer: EtherscanAPI = EtherscanAPI(ETHERSCAN_API_KEY, Network(network))
    node: NodeAPI = NodeAPI(ETHEREUM_RPC_ENDPOINT, gnosis_abi)
    builder: asset.Builder = asset.Builder(explorer, node)

    contracts: list[dict] = explorer.get_contract_source(address)

    asset_rep: asset.AssetRepresentation = builder.build_asset_rep(address=address, contract_list=contracts)

    impl_src = explorer.get_contract_source(asset_rep.get_tail_delegate_contract()["address"])[0]

    file_id: str = None

    if len(contracts) > 1:
        source_code_dict: dict = json.loads(impl_src["SourceCode"][1:-1])

        g = builder.build_dependency_graph(impl_src["ContractName"], source_code_dict["sources"])

        file_id = system.flatten_graph_to_file(source_code_dict['sources'], g)
    
    else:
        file_id = system.cache_contract(impl_src["SourceCode"])

    analyzer: CounterPartyAnalyzer = CounterPartyAnalyzer(node, gnosis_abi, ownable_abi)

    threats: list[Threat] = []

    abi = explorer.get_contract_abi(asset_rep.get_tail_delegate_contract()["address"])

    if analyzer.has_owner(abi):
        threats.append(
            Threat("Contract has privileged actor role",
                   "Token contract uses ownable schema for granting priveleged access controls",
                   "")
        )

        ## Get the owner
        owner_addr: str = node.get_owner(asset_rep.get_head_proxy_contract()["address"], abi)

        contracts: list[dict] = explorer.get_contract_source(owner_addr)

        ## Build asset representation for owner
        owner_rep: asset.AssetRepresentation = builder.build_asset_rep(address=owner_addr, contract_list=contracts)

        ## Get tail contract
        tail_contract: str = asset_rep.get_tail_delegate_contract()["address"]

        if analyzer.is_gnosis_multisig(tail_contract):
            state: GnosisState = node.get_gnosis_state(tail_contract)

            threats[0].risk = f"{state.m}/{state.n} ({state.score}) required to act maliciously"

        else:
            threats[0].risk = f"One actor is required to act maliciously"


        functions = []
        for item in abi:
            print(item)
            print(item.keys())
            if "name" in item.keys():
                functions.append(item["name"])

        
        print("Functions ",functions)
        graphs = system.generate_call_graphs(file_id, impl_src["ContractName"], functions)
        assessment = Assessment(owner_addr, [])
        
        print("Graphs ", graphs)
        for (graph, function) in enumerate(graphs):
            print("Func", function)
            print(graph)
            if "_onlyOwner" in graph:
                assessment.custodial_functions.append(function)
        
        assessment.threats = threats

    return jsonify(assessment.serialize())

    reutrn  
if __name__ == "__main__":
    app.run(debug=True)
