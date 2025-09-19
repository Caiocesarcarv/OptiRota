import json
import networkx as nx
from math import radians, sin, cos, sqrt, atan2

# Constante da Terra para cálculo da distância
RAIO_TERRA_M = 6371000

def haversine(lat1, lon1, lat2, lon2):
    """
    Calcula a distância entre dois pontos geográficos usando a fórmula de Haversine.

    Args:
        lat1 (float): Latitude do primeiro ponto.
        lon1 (float): Longitude do primeiro ponto.
        lat2 (float): Latitude do segundo ponto.
        lon2 (float): Longitude do segundo ponto.

    Returns:
        float: A distância entre os dois pontos em metros.
    """
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return RAIO_TERRA_M * c

def criar_grafo_do_json(arquivo_json):
    """
    Cria um grafo NetworkX a partir de um arquivo JSON de dados do OpenStreetMap.
    Otimizado para grandes arquivos.

    Args:
        arquivo_json (str): O caminho para o arquivo JSON.

    Returns:
        networkx.DiGraph or None: O grafo criado ou None se houver um erro.
    """
    print("")
    print("Iniciando a criação do grafo...")
    try:
        with open(arquivo_json, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except FileNotFoundError:
        print(f"Erro: O arquivo {arquivo_json} não foi encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Erro: Não foi possível decifrar o arquivo JSON {arquivo_json}.")
        return None

    grafo = nx.DiGraph()
    nodes_dict = {}

    # Primeira iteração para adicionar todos os nós (pontos)
    # e armazená-los em um dicionário para referência rápida.
    for element in dados['elements']:
        if element['type'] == 'node':
            if 'lat' in element and 'lon' in element:
                nodes_dict[element['id']] = element
                grafo.add_node(element['id'], lat=element['lat'], lon=element['lon'])

    # Segunda iteração para adicionar as arestas (ruas)
    for element in dados['elements']:
        if element['type'] == 'way' and 'tags' in element and 'highway' in element['tags']:
            if 'nodes' in element:
                node_ids = element['nodes']
                is_oneway = element['tags'].get('oneway') == 'yes'
                nome_da_rua = element['tags'].get('name', 'unknown')
                tipo_da_rua = element['tags'].get('highway', 'unclassified')

                for i in range(len(node_ids) - 1):
                    origem_id = node_ids[i]
                    destino_id = node_ids[i+1]

                    if origem_id in nodes_dict and destino_id in nodes_dict:
                        origem_coords = (nodes_dict[origem_id]['lat'], nodes_dict[origem_id]['lon'])
                        destino_coords = (nodes_dict[destino_id]['lat'], nodes_dict[destino_id]['lon'])
                        
                        peso = haversine(origem_coords[0], origem_coords[1], destino_coords[0], destino_coords[1])
                        
                        grafo.add_edge(origem_id, destino_id, weight=peso, name=nome_da_rua, highway=tipo_da_rua)
                        
                        if not is_oneway and not grafo.has_edge(destino_id, origem_id):
                            grafo.add_edge(destino_id, origem_id, weight=peso, name=nome_da_rua, highway=tipo_da_rua)

    print(f"Número de nós encontrados no arquivo: {len(nodes_dict)}")
    print(f"Número de arestas adicionadas ao grafo: {grafo.number_of_edges()}")
    print(f"¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨")
    return grafo