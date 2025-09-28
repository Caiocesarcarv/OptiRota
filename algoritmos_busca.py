import networkx as nx
from parser import haversine # Reutilizando a função de cálculo de distância

def dijkstra(grafo, origem_id, destino_id):
    try:
        caminho = nx.dijkstra_path(grafo, origem_id, destino_id, weight='weight')
        return caminho
    except nx.NetworkXNoPath:
        print(f"Não foi encontrado um caminho entre {origem_id} e {destino_id}.")
        return None

def a_estrela(grafo, origem_id, destino_id):      
    # Função de heurística: calcula a distância em linha reta (Haversine)
    def heuristica(u, v):
        lat1, lon1 = grafo.nodes[u]['lat'], grafo.nodes[u]['lon']
        lat2, lon2 = grafo.nodes[v]['lat'], grafo.nodes[v]['lon']
        return haversine(lat1, lon1, lat2, lon2)

    try:
        caminho = nx.astar_path(grafo, origem_id, destino_id, heuristic=heuristica, weight='weight')
        return caminho
    except nx.NetworkXNoPath:
        print(f"Não foi encontrado um caminho entre {origem_id} e {destino_id}.")
        return None
        
