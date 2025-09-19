# Arquivo para testar a função haversine de forma isolada.

# 1. Importa a função haversine do arquivo parser.py
from parser import haversine

# 2. Defina aqui as coordenadas dos dois pontos que você quer testar
# Exemplo: Pontos na Avenida Doutor Antônio Gouveia, Maceió, AL
lat1 = -9.676727
lon1 = -35.760080

lat2 = -9.674926
lon2 = -35.754034

# 3. Chama a função haversine com as coordenadas e armazena o resultado
distancia_em_metros = haversine(lat1, lon1, lat2, lon2)

# 4. Imprime o resultado para a sua verificação
print(f"Coordenadas do Ponto 1: ({lat1}, {lon1})")
print(f"Coordenadas do Ponto 2: ({lat2}, {lon2})")
print("---")
print(f"A distância calculada entre os dois pontos é de {distancia_em_metros:.2f} metros.")
#https://www.openstreetmap.org/#map=17/-9.676727/-35.760080
#https://www.openstreetmap.org/#map=17/-9.674929/-35.754039