import requests
import json

from enum import Enum
from src.settings import Network

"""
Helper lambda functions
"""
is_proxy = lambda contract: contract["Proxy"] == "1"

"""
Data type declarations
"""

Contract = dict


"""
Etherscan endpoints and other explorer interaction related constants
"""

ETHERSCAN_URL: str = "https://api.etherscan.io/api"

# TODO - Make these named string parameters
EXTENSION: str = "?module={0}&action={1}&address={2}&apikey={3}"

class Module(Enum):
    contract = "contract"

class Action(Enum):
    get_abi = "getabi"
    get_source = "getsourcecode"

"""
Request based constants
"""

HEADER: dict = {"Content-Type": "application/json"}

# EtherscanAPI - API client object
class EtherscanAPI:

    def __init__(self, api_key: str, net: Network) -> None:
        self.key: str = api_key
        self.net: Network = net

        self.endpoint: str = self.get_endpoint(net)
    

    def get_contract_abi(self, address: str) -> list[dict]:
        print("Getting contract ABI for ", address)
        resp = self.get_etherscan_response(address, Module.contract, Action.get_abi)
        return json.loads(resp)

    def get_contract_source(self, address: str) -> list[dict]:
        resp = self.get_etherscan_response(address, Module.contract, Action.get_source)
        return resp



    """
    Internal class helper functions
    """
    def get_endpoint(self, net: Network) -> str:
        if self.net == Network.eth:
            return ETHERSCAN_URL
        
        raise Exception("Invalid network provided", net)
    
    def get_etherscan_response(self, address: str, module: Module, action: Action) -> list[dict]:
        url: str = self.endpoint + EXTENSION.format(
                                                    module.value,
                                                    action.value,
                                                    address,
                                                    self.key
                                                )

        print(url)
        resp: requests.Response = requests.get(url, HEADER)

        if resp.status_code != 200:
            raise Exception(f"{self.net} Etherscan API request failed. Expected status code 200, got {resp.status_code}: {resp.json()}")

        resp_json: dict = resp.json()
    
        if resp_json["status"] != '1' or resp_json["message"] != "OK":
            raise Exception(f"{self.net} Etherscan API request failed with not OK status:{resp.json()}")

        return resp_json["result"]