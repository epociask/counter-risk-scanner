import json
import os
import random
import re

import subprocess
from src.solidity.compiler import SolcCompiler

"""
Variable constants
"""

TEMP_PATH: str = "/tmp/"

"""
File extensions
"""

SOLIDITY_EXT = ".sol"

rand_int = lambda : random.randint(0, 100000000000)

def remove_comments(string):
    string = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,string) # remove all occurrences streamed comments (/*COMMENT */) from string
    string = re.sub(re.compile("//.*?\n" ) ,"" ,string) # remove all occurrence single-line comments (//COMMENT\n ) from string
    return string

# Higher order system class to handle OS interfacing operations that perform system calls
class SystemAPI:

    def __init__(self) -> None:
        self.sol_compiler: SolcCompiler = SolcCompiler()
        self.cached_files: list[str] = []

    def read_file(self, name: str) -> str:
        file_name = TEMP_PATH + name + SOLIDITY_EXT

        print("Reading ", file_name)

        f = open(file_name, "r")
        lines = f.read()
        print(lines)

        return lines

    def read_json_from_file(self, fileName: str, tmp: bool=False) -> dict:
        if tmp:
            fileName = TEMP_PATH + fileName

        with open(fileName, "r") as fr:
            return json.load(fr)

    def write_file(self, name: str, contents: str):
        file_path: str = TEMP_PATH + name

        print("Writing to ", file_path)
        with open(file_path, "w") as fw:
            fw.write(contents)

        self.cached_files.append(file_path)

    # Returns success boolean indicating if file could be successfully deleted
    def delete_file(self, name: str) -> bool:
        try:
            os.remove(name)

        except Exception as e:
            print(f"Could not delete file: {e}")

    def cache_contract(self, code: str, ext: str = SOLIDITY_EXT) -> str:
        file_id: str = str(rand_int())

        self.write_file(file_id + ext, code)
        return file_id
        
    def flatten_graph_to_file(self, source_map, g) -> str:
        buffer_list: list[str] = []

        graph = g.graph
        key = g.compiled_contract

        self.graph_helper(graph, key, source_map, buffer_list)

        buffer_list.reverse()

        buffer: str = ""
        for str_buffer in buffer_list:
            # Remove import directives
            str_buffer = re.sub("(import .*;)", "", str_buffer)
            # Remove licenses
            str_buffer = re.sub("(// .*)", "", str_buffer)
            # Remove comments & add
            str_buffer = remove_comments(str_buffer)
            # Lagniappe 
            str_buffer = re.sub("(./)", "", str_buffer)
            buffer += str_buffer

        file_id: str = self.cache_contract(buffer)
        return file_id

    def graph_helper(self, graph, key, source_map, buffer_list: list[str]) -> None:
        
        found = False
        for src_key, code in source_map.items():
            if key in src_key:
                found = True

                content = source_map[src_key]["content"]
                if content not in buffer_list:
                    buffer_list.append(content)

        if not found:
            return

        children = graph[key]

        if children == None:
            return

        for child in children:
            self.graph_helper(graph, child, source_map, buffer_list)


    def generate_call_graphs(self, file_key: str, contract_name: str, functions: list) -> list:
        l = []

        source = self.read_file(file_key)
        names = []

        for m in re.finditer("(contract .+{)", source):
            names.append(m.group(0).split(" ")[1])


        print(functions)
        # for name in names:
        for func in functions:
            cmd = ["surya", "ftrace", f"{contract_name}::{func}", "all", TEMP_PATH + file_key + SOLIDITY_EXT, "--json"]
            print(cmd)
            proc: subprocess.Popen = subprocess.Popen(cmd, stdout=subprocess.PIPE)

            lines = proc.stdout.readlines()


            if "function is not present" not in str(lines):
                l.append(lines)
                functions.remove(func)

        return l 