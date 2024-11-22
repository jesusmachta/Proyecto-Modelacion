import heapq

# Definición de las coordenadas
javier_home = (54, 14)  # Calle 54, Carrera 14
andreina_home = (52, 13)  # Calle 52, Carrera 13

# Establecimientos y sus coordenadas
establishments = {
    "The Darkness": (50, 14),  # Carrera 14, Calle 50
    "La Pasión": (54, 11),      # Calle 54, Carrera 11
    "Mi Rolita": (50, 12)      # Calle 50, Carrera 12
}

# Tiempos de Javier (minutos por cuadra)
time_javier = {
    (1, 0): 4,   # Norte
    (0, 1): 4,   # Este
    (-1, 0): 4,  # Sur
    (0, -1): 4,  # Oeste
    (1, 1): 6,   # Norte y Este (Carreras 12, 13, 14)
    (1, -1): 6,  # Norte y Oeste (Carreras 12, 13, 14)
    (-1, 1): 6,  # Sur y Este (Carreras 12, 13, 14)
    (-1, -1): 6, # Sur y Oeste (Carreras 12, 13, 14)
    (0, 2): 8,   # Calles con actividad comercial
}

def dijkstra(start, graph):
    queue = []
    heapq.heappush(queue, (0, start))
    distances = {start: 0}
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        
        if current_distance > distances.get(current_node, float('inf')):
            continue
        
        for direction, time in graph[current_node].items():
            distance = current_distance + time
            
            if distance < distances.get(direction, float('inf')):
                distances[direction] = distance
                heapq.heappush(queue, (distance, direction))
    
    return distances

# Aquí podría ser necesario crear una función que represente el mapa con los tiempos dados por Javier y Andreina
def create_graph(home, time_matrix):
    graph = {}
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if (dx, dy) != (0, 0):
                new_x = home[0] + dx
                new_y = home[1] + dy
                if (new_x, new_y) not in graph:
                    graph[(new_x, new_y)] = {}
    
    # Añadir conexiones con los tiempos correspondientes
    for node in graph:
        for direction, time in time_matrix.items():
            new_node = (node[0] + direction[0], node[1] + direction[1])
            if new_node in graph:
                graph[node][new_node] = time

    return graph

# Creando los gráficos
javier_graph = create_graph(javier_home, time_javier)
andreina_graph = create_graph(andreina_home, time_javier)

# Calcular las distancias
for establishment, coord in establishments.items():
    javier_distances = dijkstra(javier_home, javier_graph)
    andreina_distances = dijkstra(andreina_home, andreina_graph)

    javier_time = javier_distances.get(coord, float('inf'))
    andreina_time = andreina_distances.get(coord, float('inf'))

    if javier_time == andreina_time:
        print(f"Ambos llegan al establecimiento {establishment} al mismo tiempo: {javier_time} minutos.")
    else:
        if javier_time < andreina_time:
            time_difference = andreina_time - javier_time
            print(f"Javier debe salir a tiempo: {javier_time} minutos, Andreína a {andreina_time} minutos. "
                  f"Andreína debe salir {time_difference + 2} minutos antes.")
        else:
            time_difference = javier_time - andreina_time
            print(f"Andreína debe salir a tiempo: {andreina_time} minutos, Javier a {javier_time} minutos. "
                  f"Javier debe salir {time_difference + 2} minutos antes.")