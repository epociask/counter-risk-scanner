import os 
import json 
from decouple import Config, RepositoryEnv
from enum import Enum

## Network parameters
class Network(Enum):
    eth = "eth"
    bsc = "bsc"

path = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../")), "config.env")
print("Path: ", path)
config = Config(RepositoryEnv(path))

ETHERSCAN_API_KEY: str = config("ETHERSCAN_API_KEY")
ETHEREUM_RPC_ENDPOINT: str = config("ETHEREUM_RPC_ENDPOINT")
BSCSCAN_API_KEY: str = config("BSC_SCAN_API_KEY")
BSCSCAN_RPC_ENDPOINT: str = config("BSC_SCAN_RPC_ENDPOINT")