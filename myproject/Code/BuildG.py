import matplotlib
import networkx as nx


def buildG(nodes, edges):
    matplotlib.rcParams['font.sans-serif'] = ['KaiTi']
    G = nx.DiGraph()
    GG = nx.DiGraph()

    for node in nodes:
        G.add_node(node.id,name = node.name,att = node.att)
        GG.add_node(node.id, name=node.name, att=node.att)
    for edge in edges:
        G.add_edge(edge.NodeStart, edge.NodeEnd, relationship=edge.att)
        GG.add_edge(edge.NodeEnd, edge.NodeStart, relationship=edge.att)

    return G, GG


def buildWG(nodes, edges):
    matplotlib.rcParams['font.sans-serif'] = ['KaiTi']
    G = nx.Graph()
    for node in nodes:
        G.add_node(node.id,name = node.name,att = node.att)
    for edge in edges:
        G.add_edge(edge.NodeStart, edge.NodeEnd, relationship=edge.att)
    return G
