import json
import operator
import math

from hashlib import sha256
from merkly.mtree import MerkleTree

log2 = lambda x : math.log10(x) / math.log10(2)

def is_power_of_2(num: int) -> bool:
    return (math.ceil(log2(num)) == math.floor(log2(num)))

def abi_hash(abi: list[dict]) -> str:
    # Extract ABI function entries and ignore all non-function entries
    reduced_abi: list[dict] = [item for item in abi if "name" in item]

    # Sort by name to ensure deterministic ordering for hash generation
    reduced_abi.sort(key=operator.itemgetter("name"))
    hashes: list[hex] = []

    # Iterate over each item and append into hash list
    for item in abi:
        encoded: bytes = json.dumps(item, sort_keys=True).encode()
        item_hash: hex = sha256_hash(encoded)
        hashes.append(item_hash)

    # Add padding to ensure tree has 2^n total entries
    while not is_power_of_2(len(hashes)):
        hashes.append(hex(0x01))

    # Generate a merkle tree for the hash list
    mt: MerkleTree = MerkleTree(hashes)

    return str(mt.root)

def sha256_hash(b: bytes) -> hex:
    hasher = sha256()
    hasher.update(b)
    
    return hasher.hexdigest()
