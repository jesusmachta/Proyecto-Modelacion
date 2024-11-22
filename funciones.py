def tiempo_caminar(calle, carrera, persona=True):
    if carrera in [12,13,14]:
        if persona:
            tiempo_cuadra = 6
        else:
            tiempo_cuadra = 8

    elif calle == 51:
        if persona:
            tiempo_cuadra = 8
        else:
            tiempo_cuadra = 10
    else:
        if persona:
            tiempo_cuadra = 4
        else:
            tiempo_cuadra = 6
    return tiempo_cuadra

def calcular_tiempo_total(inicial, destino, persona=True):
    x_inicial, y_inicial = inicial #(calle, carrera)
    x_destino, y_destino = destino #(calle, carrera)

    dist_calle = abs(x_destino - x_inicial)
    dist_carrera = abs(y_destino - y_inicial)

    tiempo_total = (dist_calle*tiempo_caminar(x_inicial, y_inicial, persona) + dist_carrera*tiempo_caminar(x_destino, y_destino, persona))

    return tiempo_total

def encontrar_trayectoria(establecimiento):
    destinos = {
        "Discoteca The Darkness": (50, 14),
        "Bar La Pasión": (54, 11),
        "Cervecería Mi Rolita": (50, 12)
    }

    posicion_javier = (54, 14)
    posicion_andreina = (52, 13)

    destino = destinos[establecimiento]

    tiempo_javier = calcular_tiempo_total(posicion_javier, destino, persona=True)
    tiempo_andreina = calcular_tiempo_total(posicion_andreina, destino, persona=False)

    if tiempo_javier > tiempo_andreina:
        # Javier tarda más
        tiempo_diferencia = tiempo_javier - tiempo_andreina
        tiempo_javier_salida = tiempo_diferencia
        tiempo_andreina_salida = 0
    elif tiempo_andreina > tiempo_javier:
        # Andreína tarda más
        tiempo_diferencia = tiempo_andreina - tiempo_javier
        tiempo_andreina_salida = tiempo_diferencia
        tiempo_javier_salida = 0
    else:
        tiempo_javier_salida = 0
        tiempo_andreina_salida = 0

    return (tiempo_javier, tiempo_andreina, tiempo_javier_salida, tiempo_andreina_salida)
