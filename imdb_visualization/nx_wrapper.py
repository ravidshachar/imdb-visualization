from .neo4j_wrapper import get_actor_couples
import networkx as nx
import matplotlib.pyplot as plt

def gen_actor_couples_graph(top_num=50, order_by="acted_together"):
    G = nx.Graph()
    couples = get_actor_couples(top_num=top_num, order_by=order_by).to_dict("records")
    for row in couples:
        if row["actor1"] not in G:
            G.add_node(row["actor1"])
        if row["actor2"] not in G:
            G.add_node(row["actor2"])
        G.add_edge(row["actor1"], row["actor2"], weight=5*row["acted_together"] + row["acted_connection"])
    return G