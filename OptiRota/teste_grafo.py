import networkx as nx
from parser import criar_grafo_do_json
from visu_grafo import visualizar_mapa_interativo

# --- LÓGICA PRINCIPAL ---
if __name__ == "__main__":
 arquivo = 'exporty.json'
 grafo_final = criar_grafo_do_json(arquivo)

 if grafo_final is not None:
    print(f"Grafo criado com sucesso! :)")
    print(f"Número de nós: {grafo_final.number_of_nodes()}")
    print(f"Número de arestas: {grafo_final.number_of_edges()}")
    
    visualizar_mapa_interativo(grafo_final)
