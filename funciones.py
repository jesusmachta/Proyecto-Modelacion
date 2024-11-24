import heapq
from grafo import create_graph  # Importar el grafo corregido
from utilidades import tiempo_caminar  # Importar tiempo_caminar


def dijkstra_with_paths(start, graph):
    queue = []
    heapq.heappush(queue, (0, start, [start]))
    distances = {start: 0}
    paths = {start: [start]}

    while queue:
        current_distance, current_node, current_path = heapq.heappop(queue)

        if current_distance > distances.get(current_node, float("inf")):
            continue

        for neighbor, time in graph[current_node].items():
            distance = current_distance + time
            if distance < distances.get(neighbor, float("inf")):
                distances[neighbor] = distance
                paths[neighbor] = current_path + [neighbor]
                heapq.heappush(queue, (distance, neighbor, current_path + [neighbor]))

    return distances, paths


def encontrar_trayectoria(establecimiento):
    destinos = {
        "Discoteca The Darkness": (50, 14),
        "Bar La Pasión": (54, 11),
        "Cervecería Mi Rolita": (50, 12),
    }

    city_graph = create_graph()
    destino = destinos[establecimiento]

    # Ejecutar Dijkstra para Javier
    javier_distances, javier_paths = dijkstra_with_paths((54, 14), city_graph)
    tiempo_javier = javier_distances[destino]
    ruta_javier = javier_paths[destino]

    # Ejecutar Dijkstra para Andreína
    andreina_distances, andreina_paths = dijkstra_with_paths((52, 13), city_graph)
    tiempo_andreina = andreina_distances[destino]
    ruta_andreina = andreina_paths[destino]

    if tiempo_javier > tiempo_andreina:
        tiempo_javier_salida = tiempo_javier - tiempo_andreina
        tiempo_andreina_salida = 0
    elif tiempo_andreina > tiempo_javier:
        tiempo_andreina_salida = tiempo_andreina - tiempo_javier
        tiempo_javier_salida = 0
    else:
        tiempo_javier_salida = tiempo_andreina_salida = 0

    return tiempo_javier, tiempo_andreina, tiempo_javier_salida, tiempo_andreina_salida, ruta_javier, ruta_andreina
