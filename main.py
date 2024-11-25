from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from funciones import encontrar_trayectoria  
import matplotlib.image as mpimg


def mostrar_resultados(destino):
    resultados = encontrar_trayectoria(destino)

    # Mostrar resultados de tiempo y diferencias
    resultado_texto = (
        f"Destino: {destino}\n"
        f"Tiempo de Javier: {resultados[0]} minutos\n"
        f"Tiempo de Andreína: {resultados[1]} minutos\n"
    )
    if resultados[2] > 0:
        resultado_texto += f"Javier debe salir {resultados[2]} minutos antes.\n"
    elif resultados[3] > 0:
        resultado_texto += f"Andreína debe salir {resultados[3]} minutos antes.\n"
    else:
        resultado_texto += "Ambos pueden salir al mismo tiempo.\n"

    # Actualizar el texto en la interfaz
    resultado_label.config(text=resultado_texto)

    # Dibujar los dos grafos
    fig_javier.clear()
    fig_andreina.clear()

    ax_javier = fig_javier.add_subplot(111)
    ax_andreina = fig_andreina.add_subplot(111)

    destino_coords = {
        "Discoteca The Darkness": (50, 14),
        "Bar La Pasión": (54, 11),
        "Cervecería Mi Rolita": (50, 12)
    }

    dibujar_grafo_javier(ax_javier, resultados[4], destino_coords[destino])  # Ruta de Javier
    dibujar_grafo_andreina(ax_andreina, resultados[5], destino_coords[destino])  # Ruta de Andreína

    canvas_javier.draw()
    canvas_andreina.draw()


def ajustar_posiciones(nodo):
    """
    Transforma las coordenadas originales (calle, carrera) al sistema ajustado del grafo.
    """
    return nodo[0] - 50, nodo[1] - 10


def dibujar_grafo_javier(ax, ruta_javier, destino):
    # Crear el grafo base
    grafo = nx.grid_2d_graph(6, 6)  # Cuadrícula (Calles 50-55, Carreras 10-15)
    pos = {(x, y): (y - 10, -(x - 50)) for x, y in grafo.nodes()}  # Ajustar posiciones para grafo

    # Crear etiquetas reales (Calle y Carrera), excluyendo nodos con íconos
    etiquetas = {
        nodo: f"Calle {nodo[0]} Cr{nodo[1]}"
        for nodo in grafo.nodes()
        if nodo != (54, 14) and nodo != destino
    }

    # Dibujar nodos y aristas base
    nx.draw(
        grafo,
        pos,
        ax=ax,
        node_size=400,
        node_color="lightgrey",
        edge_color="lightgrey",
    )
    nx.draw_networkx_labels(
        grafo,
        pos,
        labels=etiquetas,
        font_size=5,  # Reducir tamaño de la fuente
        font_color="black",
    )

    # Ajustar ruta de Javier al sistema de referencia
    ruta_javier = [ajustar_posiciones(nodo) for nodo in ruta_javier]

    # Dibujar nodo inicial (casa de Javier)
    casa_javier = ajustar_posiciones((54, 14))  # Coordenadas reales de la casa
    casa_icon = mpimg.imread("casa.png")  # Cargar el ícono de la casa
    ax.imshow(
        casa_icon,
        extent=[pos[casa_javier][0] - 0.2, pos[casa_javier][0] + 0.2,
                pos[casa_javier][1] - 0.2, pos[casa_javier][1] + 0.2],
        zorder=5
    )

    # Dibujar nodo destino (local)
    destino_ajustado = ajustar_posiciones(destino)
    local_icon = mpimg.imread("local.png")  # Cargar el ícono del local
    ax.imshow(
        local_icon,
        extent=[pos[destino_ajustado][0] - 0.2, pos[destino_ajustado][0] + 0.2,
                pos[destino_ajustado][1] - 0.2, pos[destino_ajustado][1] + 0.2],
        zorder=5
    )

    # Dibujar ruta de Javier
    if ruta_javier:
        nx.draw_networkx_nodes(grafo, pos, nodelist=ruta_javier, node_color="#ADD8E6", ax=ax)
        edges = [(ruta_javier[i], ruta_javier[i + 1]) for i in range(len(ruta_javier) - 1)]
        nx.draw_networkx_edges(grafo, pos, edgelist=edges, edge_color="#ADD8E6", width=2, ax=ax)

    ax.set_title("Ruta de Javier")


def dibujar_grafo_andreina(ax, ruta_andreina, destino):
    grafo = nx.grid_2d_graph(6, 6)  # Cuadrícula (Calles 50-55, Carreras 10-15)
    pos = {(x, y): (y - 10, -(x - 50)) for x, y in grafo.nodes()}  # Ajustar posiciones para grafo

    # Crear etiquetas reales (Calle y Carrera)
    etiquetas = {
        nodo: f"Calle {nodo[0]} Cr{nodo[1]}"
        for nodo in grafo.nodes()
        if nodo != (52, 13) and nodo != destino
    }

    # Dibujar nodos y aristas base con etiquetas reales
    nx.draw(
        grafo,
        pos,
        ax=ax,
        node_size=400,
        node_color="lightgrey",
        edge_color="lightgrey",
    )
    nx.draw_networkx_labels(
        grafo,
        pos,
        labels=etiquetas,
        font_size=5,  
        font_color="black",
    )

    # Ajustar ruta de Andreína al sistema de referencia
    ruta_andreina = [ajustar_posiciones(nodo) for nodo in ruta_andreina]

    # Dibujar nodo inicial (casa de Andreína)
    casa_andreina = ajustar_posiciones((52, 13))  # Coordenadas reales de la casa
    casa_icon = mpimg.imread("casa.png")  # Cargar el ícono de la casa
    ax.imshow(
        casa_icon,
        extent=[pos[casa_andreina][0] - 0.2, pos[casa_andreina][0] + 0.2,
                pos[casa_andreina][1] - 0.2, pos[casa_andreina][1] + 0.2],
        zorder=5
    )

    # Dibujar nodo destino (local)
    destino_ajustado = ajustar_posiciones(destino)
    local_icon = mpimg.imread("local.png")  # Cargar el ícono del local
    ax.imshow(
        local_icon,
        extent=[pos[destino_ajustado][0] - 0.2, pos[destino_ajustado][0] + 0.2,
                pos[destino_ajustado][1] - 0.2, pos[destino_ajustado][1] + 0.2],
        zorder=5
    )

    # Dibujar ruta de Andreína
    if ruta_andreina:
        nx.draw_networkx_nodes(grafo, pos, nodelist=ruta_andreina, node_color="#FF69B4", ax=ax)
        edges = [(ruta_andreina[i], ruta_andreina[i + 1]) for i in range(len(ruta_andreina) - 1)]
        nx.draw_networkx_edges(grafo, pos, edgelist=edges, edge_color="#FF69B4", width=2, ax=ax)

    ax.set_title("Ruta de Andreína")


# Crear la interfaz
root = Tk()
root.title("Planificación de Salidas de Javier y Andreína")

# Menú para seleccionar destino
destino_var = StringVar(value="Discoteca The Darkness")
ttk.Label(root, text="Seleccione el destino:").pack(pady=5)
destino_menu = ttk.Combobox(
    root,
    textvariable=destino_var,
    values=["Discoteca The Darkness", "Bar La Pasión", "Cervecería Mi Rolita"],
    state="readonly",
)
destino_menu.pack(pady=5)

# Botón para calcular resultados
ttk.Button(
    root, text="Calcular", command=lambda: mostrar_resultados(destino_var.get())
).pack(pady=10)

# Área para mostrar resultados
resultado_label = Label(root, text="", justify="left", font=("Arial", 12))
resultado_label.pack(pady=10)

# Área para grafo de Javier
fig_javier, ax_javier = plt.subplots(figsize=(3, 3))
canvas_javier = FigureCanvasTkAgg(fig_javier, master=root)
canvas_javier.get_tk_widget().pack(side=LEFT, padx=2, pady=10)

# Área para grafo de Andreína
fig_andreina, ax_andreina = plt.subplots(figsize=(3, 3))
canvas_andreina = FigureCanvasTkAgg(fig_andreina, master=root)
canvas_andreina.get_tk_widget().pack(side=RIGHT, padx=2, pady=10)

# Ejecutar la interfaz
root.mainloop()
