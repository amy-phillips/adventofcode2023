from IPython.display import SVG

import numpy as np
from scipy import sparse
import pandas as pd
import cProfile
from sknetwork.data import from_edge_list, from_adjacency_list, from_graphml, from_csv
from sknetwork.visualization import svg_graph, svg_bigraph
from sknetwork.clustering import Louvain, get_modularity, PropagationClustering

from time import time

from sklearn import metrics
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

def try_louvain(graph):
    adjacency = graph.adjacency
    names = graph.names
    image = svg_graph(adjacency, names=names, width=3072, height=1024, filename="parsed.svg")

    # do some things....?
    louvain = Louvain(resolution = 0.8)
    labels = louvain.fit_predict(adjacency)

    labels_unique, counts = np.unique(labels, return_counts=True)
    print(labels_unique, counts)

    image = svg_graph(adjacency, labels=labels, width=3072, height=1024, filename="splitted.svg")

    if counts.size==2:
        print(f"Two groups found {counts[0]} and {counts[1]} => {counts[0]*counts[1]}") 
    
def try_propagation(graph):
    adjacency = graph.adjacency
    propagation = PropagationClustering(n_iter=-1)
    labels = propagation.fit_predict(adjacency)
    print(labels)

    labels_unique, counts = np.unique(labels, return_counts=True)
    print(labels_unique, counts)

    image = svg_graph(adjacency, labels=labels, width=3072, height=1024, filename="propagated.svg")


    if counts.size==3:
        print(f"Three groups found {counts[0]} and {counts[1]} and {counts[2]} => {(counts[0]+counts[2])*counts[1]} or maybe {(counts[0]+counts[1])*counts[2]}") 

def run(_input:str):
    # parse the connections into an adjacency dict
    adjacency_dict = {}
    for line in _input.split('\n'):
        name,links = line.split(':')
        adjacency_dict[name] = []
        links = links.split()
        for link in links:
            adjacency_dict[name].append(link.strip())

    graph = from_adjacency_list(adjacency_dict, directed=False)

    #try_louvain(graph)   

    try_propagation(graph)   
    


with open("day25_actual_input.txt", "r") as f:
    #cProfile.run("run(f.read())")
    run(f.read())
