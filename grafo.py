from utilidades import tiempo_caminar  # Importar la función para calcular tiempos

def create_graph():
    graph = {}
    for calle in range(50, 56):  # Calles 50 a 55
        for carrera in range(10, 16):  # Carreras 10 a 15
            graph[(calle, carrera)] = {}

    for node in graph:
        calle, carrera = node
        neighbors = [
            (calle + 1, carrera),  # Norte
            (calle - 1, carrera),  # Sur
            (calle, carrera + 1),  # Este
            (calle, carrera - 1),  # Oeste
        ]
        for neighbor in neighbors:
            if neighbor in graph:
                graph[node][neighbor] = tiempo_caminar(calle, carrera)
    return graph
