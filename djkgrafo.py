#imports
from pyamaze import maze, agent
import heapq
import networkx as nx
import matplotlib.pyplot as plt

#maze
lab = maze()
lab.CreateMaze()

def grafo_build(lab):
    grafo = {}

    for linha, coluna, in lab.maze_map:
        cell = (linha, coluna) #estrutura do lab
        grafo[cell] = []

        for dir, free in lab.maze_map[cell].items():
            if free:
                if dir == 'N':
                    vizinho = (linha-1, coluna)
                elif dir == 'S':
                    vizinho = (linha+1, coluna)
                elif dir == 'E':
                    vizinho = (linha, coluna+1)
                elif dir == 'W':
                    vizinho = (linha, coluna-1)
                grafo[cell].append(vizinho)
    return grafo

grafo = grafo_build(lab)

for cell, vizinhos in grafo.items():
    print(f'Célula {cell} -> Vizinhos {vizinhos}')
    
def dijkstra(grafo, strat, goal):
    dist = {start: 0}
    prev = {}
    pq = [(0, start)]

    while pq:
        custo_atual, atual = heapq.heappop(pq)

        if atual == goal:
            break

        for vizinho in grafo.get(atual, []):
            novo_custo = custo_atual + 1
            if vizinho not in dist or novo_custo < dist[vizinho]:
                dist[vizinho] = novo_custo
                prev[vizinho] = atual
                heapq.heappush(pq, (novo_custo, vizinho))

    caminho = []
    cell = goal
    while cell in prev:
        caminho.append(cell)
        cell= prev[cell]
    caminho.append(start)
    caminho.reverse()

    return caminho if goal in dist else None

start = (10, 5)
goal = (1, 1)

caminho = dijkstra(grafo, start, goal)

if caminho:
    print(f'Caminho encontrado: {caminho}')
    robot = agent(lab, start[0], start[1], footprints=True)
    lab.tracePath({robot:caminho}, delay=600)
else:
    print('Caminho não encontrado.')
    

def grafo_show(grafo):
    G = nx.Graph()

    #arestas
    for nodo, vizinhos in grafo.items():
        for vizinho in vizinhos:
            G.add_edge(nodo ,vizinho)

    plt.figure(figsize=(6,6))

    pos = {node:(node[1], -node[0]) for node in G.nodes()}
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500)
    
    #destarcar caminho encontrado
    if caminho:
        caminho_arestas = [(caminho[i], caminho[i+1]) for i in range(len(caminho)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=caminho_arestas, edge_color='red', width=3)
    
    plt.show()

grafo_show(grafo)

lab.run()