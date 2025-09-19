import folium
from parser import criar_grafo_do_json

# Mapeia os tipos de rodovia para diferentes espessuras de linha
tipo_de_estrada_peso = {
    'motorway': 4,
    'trunk': 4,
    'primary': 3.5,
    'secondary': 3,
    'tertiary': 2.5,
    'residential': 2,
    'service': 1.5,
    'unclassified': 1.5,
    'living_street': 1.5,
    'footway': 1,
    'path': 1
}
tipo_de_estrada_cor = {
    'motorway': 'red', 'trunk': 'red', 'primary': 'orange', 'secondary': 'purple',
    'tertiary': 'black', 'residential': 'blue', 'service': 'green',
    'unclassified': 'green', 'living_street': 'green', 'footway': 'gray', 'path': 'gray'
}

# --- LÓGICA PRINCIPAL ---
def visualizar_mapa_interativo(grafo):
    """
    Cria e salva um mapa interativo em HTML a partir do grafo.
    """
    if grafo is None:
        print("Erro: O grafo não pode ser nulo para visualização.")
        return

    # Coordenadas do centro do seu grafo para centralizar o mapa
    coords_centro = (
        sum(data['lat'] for _, data in grafo.nodes(data=True)) / grafo.number_of_nodes(),
        sum(data['lon'] for _, data in grafo.nodes(data=True)) / grafo.number_of_nodes()
    )
    # Cria o mapa usando Folium com um zoom inicial ajustado
    m = folium.Map(location=coords_centro, zoom_start=15)

    # Adiciona os nós (pontos) ao mapa com tooltip mais detalhado
    for node, data in grafo.nodes(data=True):
        folium.CircleMarker(
            location=[data['lat'], data['lon']],
            radius=1,
            color='blue',
            fill=True,
            fill_color='blue',
            tooltip=f"ID: {node}<br>Lat: {data['lat']}<br>Lon: {data['lon']}"
        ).add_to(m)

    # Adiciona as arestas (ruas) ao mapa com espessuras diferentes
    for origem, destino, data in grafo.edges(data=True):
        origem_coords = (grafo.nodes[origem]['lat'], grafo.nodes[origem]['lon'])
        destino_coords = (grafo.nodes[destino]['lat'], grafo.nodes[destino]['lon'])

        # Obtém o tipo de rodovia e define o peso da linha, com valor padrão 1.5
        tipo_estrada = data.get('highway', 'unclassified')
        peso_linha = tipo_de_estrada_peso.get(tipo_estrada, 1.5)
        cor_linha = tipo_de_estrada_cor.get(tipo_estrada, 'gray')
        
        folium.PolyLine(
            locations=[origem_coords, destino_coords],
            color=cor_linha,
            weight=peso_linha,
            opacity=0.7,
            tooltip=data.get('name', 'Sem nome')
        ).add_to(m)

    # Salva o mapa em um arquivo HTML
    m.save('mapa_interativo.html')
    print("...Mapa interativo salvo como 'mapa_interativo.html'. Abra-o no seu navegador.")
    print("")