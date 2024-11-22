from funciones import *

def main():
    print("Bienvenido al sistema de planificación de salidas de Javier y Andreina.")
    while True:
        establecimiento = int(input("Ingrese el número del establecimiento que desea visitar:\n1- Bar La Pasión\n2- Discoteca The Darkness\n3- Cervecería Mi Rolita\n4- Salir\n=> "))
        print("\n")
        if establecimiento == 1:
            establecimiento = "Bar La Pasión"
        elif establecimiento == 2:
            establecimiento = "Discoteca The Darkness"
        elif establecimiento == 3:
            establecimiento = "Cervecería Mi Rolita"
        elif establecimiento == 4:
            print("Gracias por usar el sistema de planificación de salidas de Javier y Andreina.")
            break
        else:
            print("Establecimiento no válido.")
            print("\n")
            continue
        
        resultados = encontrar_trayectoria(establecimiento)

        print(f"Tiempo Javier: {resultados[0]} minutos")
        print(f"Tiempo Andreína: {resultados[1]} minutos")
        print("\n")

        if resultados[2] > 0:
            print(f"Javier debe salir {resultados[2]} minutos antes.")
            print("\n")
        elif resultados[3] > 0:
            print(f"Andreína debe salir {resultados[3]} minutos antes.")
            print("\n")
        else:
            print("Ambos pueden salir al mismo tiempo.")
            print("\n")

main()