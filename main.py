from src.settings import (ETHERSCAN_API_KEY, ETHEREUM_RPC_ENDPOINT)
from src.settings import Network
from src.clients.etherscan import EtherscanAPI
from src.clients.node import (NodeAPI, GnosisState)

from src.analyzers.counterparty import CounterPartyAnalyzer

import src.utils as utils

from argparse import ArgumentParser

def get_arg_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Assess tokenized asset for counterparty risk")
    parser.add_argument("-a", "--address", type=str,
                    help="On-chain contract address")
    parser.add_argument("-n", "--network", type=str,
                    help="EVM network to use; currently supports eth, bsc")

    return parser

def main():
    parser: ArgumentParser = get_arg_parser()
    args: object = parser.parse_args()

    gnosis_abi: list[dict] = utils.read_json_from_file("abi/gnosis_multisig.json")
    ownable_abi: list[dict] = utils.read_json_from_file("abi/ownable.json")

    explorer: EtherscanAPI = EtherscanAPI(ETHERSCAN_API_KEY, Network(args.network))
    node: NodeAPI = NodeAPI(ETHEREUM_RPC_ENDPOINT, gnosis_abi)

    analyzer: CounterPartyAnalyzer = CounterPartyAnalyzer(gnosis_abi, ownable_abi)

    contract_abi: list[dict] = explorer.get_contract_abi(args.address)

    # TODO - Figure out the best way to chain this all together
    if analyzer.has_owner(contract_abi):
        owner = node.get_owner(args.address, contract_abi)
        print("Owner address ", owner)
    
    source = explorer.get_contract_source(args.address)
    found, address = analyzer.get_proxy(source)
    if found:
        contract_abi: list[dict] = explorer.get_contract_abi(args.address)

    multisig = analyzer.is_gnosis_multisig(contract_abi)
    print("Gnosis? ", multisig)




    if analyzer.is_gnosis_multisig(contract_abi):
        state: GnosisState = node.get_gnosis_state(args.address)
        print("State ", state)

    print("Is Ownable: ", analyzer.has_owner(contract_abi))

if __name__ == "__main__":
    main()