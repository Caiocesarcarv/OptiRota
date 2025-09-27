import networkx as nx
import folium
import random
from parser import criar_grafo_do_json
from algoritmos_busca import dijkstra, a_estrela

def visualizar_mapa_com_rota(grafo, caminho=None, nome_arquivo='mapa_com_rota.html'):
    """
    Cria e salva um mapa interativo em HTML, destacando uma rota específica.
    """
    if grafo is None:
        print("Erro: O grafo não pode ser nulo para visualização.")
        return

    coords_centro = (
        sum(data['lat'] for _, data in grafo.nodes(data=True)) / grafo.number_of_nodes(),
        sum(data['lon'] for _, data in grafo.nodes(data=True)) / grafo.number_of_nodes()
    )
    m = folium.Map(location=coords_centro, zoom_start=15)

    # Adiciona as arestas do grafo
    for origem, destino, data in grafo.edges(data=True):
        origem_coords = (grafo.nodes[origem]['lat'], grafo.nodes[origem]['lon'])
        destino_coords = (grafo.nodes[destino]['lat'], grafo.nodes[destino]['lon'])
        folium.PolyLine(
            locations=[origem_coords, destino_coords],
            color='gray',
            weight=1,
            opacity=0.7
        ).add_to(m)

    # Destaca o caminho encontrado
    if caminho:
        pontos_caminho = []
        for node_id in caminho:
            pontos_caminho.append((grafo.nodes[node_id]['lat'], grafo.nodes[node_id]['lon']))
        
        folium.PolyLine(
            locations=pontos_caminho,
            color='red',
            weight=5,
            opacity=1.0,
            tooltip='Rota Calculada'
        ).add_to(m)

    m.save(nome_arquivo)
    print(f"...Mapa com a rota salvo como '{nome_arquivo}'. Abra-o no seu navegador.")
    print("")

if __name__ == "__main__":
    arquivo = 'exporty.json'
    grafo_final = criar_grafo_do_json(arquivo)

    if grafo_final is not None and grafo_final.number_of_nodes() > 0:
        print(f"Grafo criado com sucesso! :)")
        
        # Escolhe dois nós aleatórios do grafo para definir uma rota
        nos_disponiveis = list(grafo_final.nodes)
        no_origem = random.choice(nos_disponiveis)
        no_destino = random.choice(nos_disponiveis)
        
        print(f"Calculando rota de {no_origem} para {no_destino}...")

        # --- Testando Dijkstra ---
        print("\n--- Executando Dijkstra ---")
        caminho_dijkstra = dijkstra(grafo_final, no_origem, no_destino)
        if caminho_dijkstra:
            print(f"Caminho encontrado com Dijkstra: {len(caminho_dijkstra)} nós.")
            visualizar_mapa_com_rota(grafo_final, caminho_dijkstra, 'mapa_rota_dijkstra.html')

        # --- Testando A* ---
        print("\n--- Executando A* (A-Estrela) ---")
        caminho_a_estrela = a_estrela(grafo_final, no_origem, no_destino)
        if caminho_a_estrela:
            print(f"Caminho encontrado com A*: {len(caminho_a_estrela)} nós.")
            visualizar_mapa_com_rota(grafo_final, caminho_a_estrela, 'mapa_rota_a_estrela.html')

        # Comparação (os caminhos devem ser idênticos em um grafo com pesos consistentes)
        if caminho_dijkstra and caminho_a_estrela:
            if caminho_dijkstra == caminho_a_estrela:
                print("\nOs caminhos encontrados por Dijkstra e A* são idênticos, como esperado.")
            else:
                print("\nAlerta: Os caminhos encontrados por Dijkstra e A* são diferentes.")