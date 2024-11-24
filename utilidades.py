def tiempo_caminar(calle, carrera, persona=True):
    # Define los tiempos por tipo de calle o carrera
    if carrera in [12, 13, 14]:  # Carreras con aceras en mal estado
        tiempo_cuadra = 6 if persona else 8
    elif calle == 51:  # Calle comercial
        tiempo_cuadra = 8 if persona else 10
    else:  # Calles y carreras normales
        tiempo_cuadra = 4 if persona else 6
    return tiempo_cuadra
