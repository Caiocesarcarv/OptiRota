import networkx as nx
import time
from parser import criar_grafo_do_json
from algoritmos_busca import dijkstra, a_estrela

def calcular_peso_total_caminho(grafo, caminho):
    """
    Calcula o peso total (distância em metros) de um caminho no grafo.
    
    Args:
        grafo: Grafo do NetworkX
        caminho: Lista de IDs dos nós que formam o caminho
    
    Returns:
        float: Distância total do caminho em metros
    """
    if caminho is None or len(caminho) < 2:
        return 0
    
    peso_total = 0
    for i in range(len(caminho) - 1):
        origem = caminho[i]
        destino = caminho[i+1]
        
        # Obtém o peso da aresta entre os dois nós
        if grafo.has_edge(origem, destino):
            peso_aresta = grafo[origem][destino].get('weight', 0)
            peso_total += peso_aresta
    
    return peso_total

def executar_dijkstra_todos_pontos(grafo, algoritmo='dijkstra', max_pontos=None):
    """
    Executa o algoritmo de busca a partir de cada nó do grafo.
    
    Args:
        grafo: Grafo do NetworkX
        algoritmo: 'dijkstra' ou 'a_estrela'
        max_pontos: Número máximo de pontos a analisar (para testes)
    
    Returns:
        dict: Dicionário com {ponto_partida: {tempo_total, resultados_por_destino}}
    """
    
    # Seleciona todos os nós ou uma amostra limitada
    todos_pontos = list(grafo.nodes())
    if max_pontos and max_pontos < len(todos_pontos):
        # Amostra aleatória para testes rápidos
        import random
        pontos_analise = random.sample(todos_pontos, max_pontos)
        print(f"Modo teste: Analisando {max_pontos} pontos de {len(todos_pontos)} totais")
    else:
        pontos_analise = todos_pontos
    
    resultados_gerais = {}
    total_pontos = len(pontos_analise)
    
    print(f"Iniciando analise com {algoritmo.upper()} para {total_pontos} pontos...")
    print("=" * 60)
    
    inicio_geral = time.time()
    
    for indice, ponto_partida in enumerate(pontos_analise, 1):
        print(f"Processando ponto {indice}/{total_pontos}: {ponto_partida}")
        
        inicio_ponto = time.time()
        resultados_ponto = {
            'tempo_total': 0,
            'caminhos_validos': 0,
            'caminhos_invalidos': 0,
            'detalhes': {}
        }
        
        # Executa busca para cada ponto de destino
        for ponto_destino in pontos_analise:
            if ponto_partida == ponto_destino:
                continue
            
            if algoritmo == 'dijkstra':
                caminho = dijkstra(grafo, ponto_partida, ponto_destino)
            else:
                caminho = a_estrela(grafo, ponto_partida, ponto_destino)
            
            if caminho:
                peso_caminho = calcular_peso_total_caminho(grafo, caminho)
                resultados_ponto['tempo_total'] += peso_caminho
                resultados_ponto['caminhos_validos'] += 1
                resultados_ponto['detalhes'][ponto_destino] = {
                    'distancia': peso_caminho,
                    'num_arestas': len(caminho) - 1
                }
            else:
                resultados_ponto['caminhos_invalidos'] += 1
                resultados_ponto['detalhes'][ponto_destino] = {'distancia': float('inf'), 'num_arestas': 0}
        
        tempo_ponto = time.time() - inicio_ponto
        resultados_ponto['tempo_execucao'] = tempo_ponto
        
        resultados_gerais[ponto_partida] = resultados_ponto
        
        print(f"   Caminhos validos: {resultados_ponto['caminhos_validos']}")
        print(f"   Caminhos invalidos: {resultados_ponto['caminhos_invalidos']}")
        print(f"   Distancia total: {resultados_ponto['tempo_total']:.2f} metros")
        print(f"   Tempo execucao: {tempo_ponto:.2f} segundos")
        print("-" * 40)
    
    tempo_total_execucao = time.time() - inicio_geral
    print(f"Analise concluida em {tempo_total_execucao:.2f} segundos")
    
    return resultados_gerais

def encontrar_melhor_ponto(resultados):
    """
    Encontra o ponto de partida com menor distância total.
    
    Args:
        resultados: Dicionário com resultados da execução
    
    Returns:
        tuple: (melhor_ponto, menor_distancia, ranking)
    """
    if not resultados:
        return None, float('inf'), []
    
    # Filtra pontos que têm caminhos válidos
    pontos_validos = {ponto: dados for ponto, dados in resultados.items() 
                     if dados['caminhos_validos'] > 0}
    
    if not pontos_validos:
        print("Nenhum ponto com caminhos validos encontrado!")
        return None, float('inf'), []
    
    # Encontra o melhor ponto (menor distância total)
    melhor_ponto = min(pontos_validos.keys(), key=lambda x: pontos_validos[x]['tempo_total'])
    menor_distancia = pontos_validos[melhor_ponto]['tempo_total']
    
    # Cria ranking ordenado
    ranking = sorted([(ponto, dados['tempo_total']) for ponto, dados in pontos_validos.items()], key=lambda x: x[1])
    
    return melhor_ponto, menor_distancia, ranking

def salvar_resultados(resultados, arquivo_saida='resultados_dijkstra.json'):
    """
    Salva os resultados em arquivo JSON para análise posterior.
    """
    import json
    
    # Converte para formato serializável
    resultados_serializaveis = {}
    for ponto, dados in resultados.items():
        resultados_serializaveis[str(ponto)] = {
            'tempo_total': dados['tempo_total'],
            'caminhos_validos': dados['caminhos_validos'],
            'caminhos_invalidos': dados['caminhos_invalidos'],
            'tempo_execucao': dados['tempo_execucao']
        }
    
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        json.dump(resultados_serializaveis, f, indent=2, ensure_ascii=False)
    
    print(f"Resultados salvos em: {arquivo_saida}")

def gerar_relatorio(resultados, grafo, arquivo_relatorio='relatorio_analise.txt'):
    """
    Gera um relatório detalhado da análise.
    """
    melhor_ponto, menor_distancia, ranking = encontrar_melhor_ponto(resultados)
    
    with open(arquivo_relatorio, 'w', encoding='utf-8') as f:
        f.write("RELATORIO DE ANALISE - MELHOR PONTO DE PARTIDA\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("ESTATISTICAS GERAIS:\n")
        f.write(f"- Total de pontos analisados: {len(resultados)}\n")
        f.write(f"- Melhor ponto de partida: {melhor_ponto}\n")
        f.write(f"- Distancia total minima: {menor_distancia:.2f} metros\n")
        f.write(f"- Distancia total minima: {menor_distancia/1000:.2f} km\n\n")
        
        if melhor_ponto:
            coords = grafo.nodes[melhor_ponto]
            f.write("COORDENADAS DO MELHOR PONTO:\n")
            f.write(f"- Latitude: {coords['lat']}\n")
            f.write(f"- Longitude: {coords['lon']}\n\n")
        
        f.write("TOP 10 MELHORES PONTOS:\n")
        for i, (ponto, distancia) in enumerate(ranking[:10], 1):
            f.write(f"{i}. Ponto {ponto}: {distancia:.2f} metros ({distancia/1000:.2f} km)\n")
        
        f.write(f"\nESTATISTICAS DETALHADAS:\n")
        distancias = [dados['tempo_total'] for dados in resultados.values() 
                     if dados['caminhos_validos'] > 0]
        if distancias:
            f.write(f"- Media de distancia: {sum(distancias)/len(distancias):.2f} metros\n")
            f.write(f"- Maior distancia: {max(distancias):.2f} metros\n")
            f.write(f"- Menor distancia: {min(distancias):.2f} metros\n")
    
    print(f"Relatorio gerado: {arquivo_relatorio}")

# --- EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    print("DESENVOLVEDOR 2: EXECUTANDO DIJKSTRA PARA TODOS OS PONTOS")
    print("=" * 60)
    
    # 1. Carregar o grafo
    arquivo_json = 'exporty.json'
    print("Carregando grafo...")
    grafo = criar_grafo_do_json(arquivo_json)
    
    if grafo is None:
        print("Erro ao carregar o grafo!")
        exit(1)
    
    print(f"Grafo carregado: {grafo.number_of_nodes()} nos, {grafo.number_of_edges()} arestas")
    
    # 2. Executar análise (usando max_pontos=10 para teste rápido - remover para análise completa)
    resultados = executar_dijkstra_todos_pontos(grafo, algoritmo='dijkstra', max_pontos=int(input("Quantos pontos será analisados?\n-> ")))
    
    # 3. Encontrar melhor ponto
    melhor_ponto, menor_distancia, ranking = encontrar_melhor_ponto(resultados)
    
    # 4. Exibir resultados
    print("\nRESULTADOS FINAIS:")
    print("=" * 40)
    if melhor_ponto:
        coords = grafo.nodes[melhor_ponto]
        print(f"MELHOR PONTO DE PARTIDA: {melhor_ponto}")
        print(f"Coordenadas: ({coords['lat']}, {coords['lon']})")
        print(f"Distancia total: {menor_distancia:.2f} metros ({menor_distancia/1000:.2f} km)")
        
        print(f"\nTOP 5 MELHORES PONTOS:")
        for i, (ponto, distancia) in enumerate(ranking[:5], 1):
            print(f"{i}. Ponto {ponto}: {distancia:.2f} metros")
    else:
        print("Nao foi possivel determinar o melhor ponto.")
    
    # 5. Salvar resultados
    salvar_resultados(resultados)
    gerar_relatorio(resultados, grafo)
    
    print("\nAnalise do Desenvolvedor 2 concluida!")
