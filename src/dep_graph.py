#Python program to print topological sorting of a DAG
from collections import defaultdict
 
#Class to represent a graph
class Graph:
    def __init__(self,vertices):
        self.graph = defaultdict(list) #dictionary containing adjacency List
        self.V = vertices #No. of vertices
 
    # function to add an edge to graph
    def add_ege(self, u: any, v: any):
        self.graph[u].append(v)
        self.compiled_contract = ""
 
    # A recursive function used by topologicalSort
    def top_sort_util(self, v, visited, stack):
 
        # Mark the current node as visited.
        visited[v] = True
 
        # Recur for all the vertices adjacent to this vertex
        for edged_vertex in self.graph[v]:
            if edged_vertex not in visited:
                self.top_sort_util(edged_vertex, visited, stack)
 
        # Push current vertex to stack which stores result
        stack.insert(0, v)
 
    # The function to do Topological Sort. It uses recursive
    # topologicalSortUtil()
    def toplogical_sort(self) -> list:
        # Mark all the vertices as not visited
        visited: bool = {}
        stack: list = []
 
        # Call the recursive helper function to store Topological
        # Sort starting from all vertices one by one
        for vertex in list(self.graph.keys()):
            if vertex not in visited:
                self.top_sort_util(vertex, visited, stack)
 
        # Print contents of stack
        return stack
        
    def __repr__(self):
        return str(self.graph)