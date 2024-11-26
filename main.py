import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import networkx as nx
from funciones import encontrar_trayectoria
import matplotlib.image as mpimg


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Planificación de Salidas de Javier y Andreína")
        self.setGeometry(100, 100, 1200, 900)

        # Widget principal
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet("background-color: gray;")

        # Layout principal
        self.layout = QVBoxLayout(self.central_widget)

        # Título y descripción
        self.label_titulo = QLabel("Javier y Andreína, seleccionen el destino de su próxima cita!", self)
        self.label_titulo.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_titulo)

        # Contenedor para el dropdown y los botones
        self.dropdown_layout = QHBoxLayout()
        self.dropdown_layout.setAlignment(Qt.AlignCenter)
 
        # Dropdown
        self.combo_destino = QComboBox(self)
        self.combo_destino.addItems(["Discoteca The Darkness", "Bar La Pasión", "Cervecería Mi Rolita"])
        self.combo_destino.setStyleSheet("font-size: 12px; padding: 5px; background-color: white; border-radius: 5px;")
        self.combo_destino.setFixedWidth(300)
        self.dropdown_layout.addWidget(self.combo_destino)

        # Botón 'calcular' 
        self.button_calcular = QPushButton("Calcular", self)
        self.button_calcular.setStyleSheet("font-size: 12px; padding: 5px;color: #FFFFFF; background-color: #FF69B4; border-radius: 5px;")
        self.button_calcular.setFixedWidth(200)
        self.button_calcular.clicked.connect(self.calcular_ruta)
        self.dropdown_layout.addWidget(self.button_calcular)

        # Botón 'ver unión'
        self.button_union = QPushButton("Ver Unión", self)
        self.button_union.setStyleSheet("font-size: 12px; padding: 5px; background-color: #FF69B4; color: #FFFFFF; border-radius: 5px;")
        self.button_union.setFixedWidth(200)
        self.button_union.clicked.connect(self.abrir_union)
        self.dropdown_layout.addWidget(self.button_union)

        # Agregar dropdown y botones al layout principal
        self.layout.addLayout(self.dropdown_layout)

        # Resultados
        self.label_resultados = QLabel("", self)
        self.label_resultados.setStyleSheet("font-size: 12px; color: white;")
        self.label_resultados.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_resultados)

        # Gráficos para los dos grafos
        self.fig_javier = Figure(figsize=(7, 7))
        self.canvas_javier = FigureCanvas(self.fig_javier)
        self.layout.addWidget(self.canvas_javier)

        self.fig_andreina = Figure(figsize=(7, 7))
        self.canvas_andreina = FigureCanvas(self.fig_andreina)
        self.layout.addWidget(self.canvas_andreina)

        self.resultados_union = None

    def calcular_ruta(self):
        destino = self.combo_destino.currentText()

        # Coordenadas de destino
        destino_coords = {
            "Discoteca The Darkness": (50, 14),
            "Bar La Pasión": (54, 11),
            "Cervecería Mi Rolita": (50, 12)
        }

        # Obtener rutas
        resultados = encontrar_trayectoria(destino)

        # Calcular quién debe salir antes
        if resultados[2] > 0:
            mensaje_tiempo = f"Javier debe salir {resultados[2]} minutos antes."
        elif resultados[3] > 0:
            mensaje_tiempo = f"Andreína debe salir {resultados[3]} minutos antes."
        else:
            mensaje_tiempo = "Ambos pueden salir al mismo tiempo."

        # Actualizar resultados
        self.label_resultados.setText(
            f"Destino: {destino}\n"
            f"Tiempo de Javier: {resultados[0]} minutos\n"
            f"Tiempo de Andreína: {resultados[1]} minutos\n"
            f"{mensaje_tiempo}"
        )

        # Dibujar rutas
        self.dibujar_grafo(self.fig_javier, self.canvas_javier, resultados[4], destino_coords[destino], "Ruta de Javier", "#B3E5FC")
        self.dibujar_grafo(self.fig_andreina, self.canvas_andreina, resultados[5], destino_coords[destino], "Ruta de Andreína", "#FFCDD2")

        # Guardar resultados para la unión
        self.resultados_union = resultados

    def abrir_union(self):
        if self.resultados_union is None:   # Si no hay resultados, no se puede abrir la ventana de unión
            self.label_resultados.setText("Primero debes calcular las rutas de Javier y Andreína.")
            self.label_resultados.setStyleSheet("font-size: 12px; color: white;") 
        else: 
            self.union_window = UnionWindow(self.resultados_union)
            self.union_window.show()

    def dibujar_grafo(self, fig, canvas, ruta, destino, titulo, color):
        fig.clear()
        ax = fig.add_subplot(111)

        # Crear el grafo base
        grafo = nx.grid_2d_graph(6, 6)  # Calles 50-55, Carreras 10-15
        pos = {(x, y): (y - 10, -(x - 50)) for x, y in grafo.nodes()}  # Ajustar posiciones

        # Dibujar nodos y aristas base
        nx.draw(
            grafo,
            pos,
            ax=ax,
            node_size=700,
            node_color="lightgrey",
            edge_color="lightgrey",
        )

        # Dibujar íconos de inicio y destino
        casa_icon = mpimg.imread("casa.png")
        local_icon = mpimg.imread("local.png")

        casa_inicio = (54, 14) if "Javier" in titulo else (52, 13)
        casa_inicio = (casa_inicio[0] - 50, casa_inicio[1] - 10)
        destino_ajustado = (destino[0] - 50, destino[1] - 10)

        ax.imshow(
            casa_icon,
            extent=[pos[casa_inicio][0] - 0.2, pos[casa_inicio][0] + 0.2,
                    pos[casa_inicio][1] - 0.2, pos[casa_inicio][1] + 0.2],
            zorder=5
        )
        ax.imshow(
            local_icon,
            extent=[pos[destino_ajustado][0] - 0.2, pos[destino_ajustado][0] + 0.2,
                    pos[destino_ajustado][1] - 0.2, pos[destino_ajustado][1] + 0.2],
            zorder=5
        )

        # Dibujar ruta
        ruta_ajustada = [(n[0] - 50, n[1] - 10) for n in ruta]
        if ruta_ajustada:
            nx.draw_networkx_nodes(grafo, pos, nodelist=ruta_ajustada, node_color=color, ax=ax)
            edges = [(ruta_ajustada[i], ruta_ajustada[i + 1]) for i in range(len(ruta_ajustada) - 1)]
            nx.draw_networkx_edges(grafo, pos, edgelist=edges, edge_color=color, width=2, ax=ax)

        # Agregar etiquetas dentro de los nodos
        etiquetas = {(x, y): f"C{x+50},Cr{y+10}" for x, y in grafo.nodes() if (x, y) != casa_inicio and (x, y) != destino_ajustado}
        nx.draw_networkx_labels(grafo, pos, etiquetas, font_color='black', font_size=6, ax=ax)

        # Agregar etiquetas dentro de los nodos ruta
        #labels = {(x, y): f"C{x+50},Cr{y+10}" for x, y in grafo.nodes() if (x,y) != casa_inicio and (x, y) != destino_ajustado and (x, y) in ruta_ajustada}
        #nx.draw_networkx_labels(grafo, pos, labels, font_color='black', font_size=6, ax=ax)

        ax.set_title(titulo, fontsize=12)
        ax.axis("off")
        canvas.draw()


class UnionWindow(QMainWindow):
    def __init__(self, resultados):
        super().__init__()
        self.setWindowTitle("Unión de Rutas de Javier y Andreína")
        self.setGeometry(150, 150, 800, 600)

        # Widget principal
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout principal
        self.layout = QVBoxLayout(self.central_widget)

        # Gráfico para la unión de las rutas
        self.fig_union = Figure(figsize=(7, 7))
        self.canvas_union = FigureCanvas(self.fig_union)
        self.layout.addWidget(self.canvas_union)

        # Dibujar la unión de las rutas
        self.dibujar_union(resultados)

    def dibujar_union(self, resultados):
        fig = self.fig_union
        canvas = self.canvas_union
        fig.clear()
        ax = fig.add_subplot(111)

        # Crear el grafo base
        grafo = nx.grid_2d_graph(6, 6)  # Calles 50-55, Carreras 10-15
        pos = {(x, y): (y - 10, -(x - 50)) for x, y in grafo.nodes()}  # Ajustar posiciones

        # Dibujar nodos y aristas base
        nx.draw(
            grafo,
            pos,
            ax=ax,
            node_size=700,
            node_color="lightgrey",
            edge_color="lightgrey",
        )

        # Dibujar íconos de inicio y destino
        casa_icon = mpimg.imread("casa.png")
        local_icon = mpimg.imread("local.png")

        casa_inicio_javier = (54, 14)
        casa_inicio_andreina = (52, 13)
        destino = resultados[4][-1]  # Último nodo de la ruta de Javier (o Andreína)

        casa_inicio_javier = (casa_inicio_javier[0] - 50, casa_inicio_javier[1] - 10)
        casa_inicio_andreina = (casa_inicio_andreina[0] - 50, casa_inicio_andreina[1] - 10)
        destino_ajustado = (destino[0] - 50, destino[1] - 10)

        ax.imshow(
            casa_icon,
            extent=[pos[casa_inicio_javier][0] - 0.2, pos[casa_inicio_javier][0] + 0.2,
                    pos[casa_inicio_javier][1] - 0.2, pos[casa_inicio_javier][1] + 0.2],
            zorder=5
        )
        ax.imshow(
            casa_icon,
            extent=[pos[casa_inicio_andreina][0] - 0.2, pos[casa_inicio_andreina][0] + 0.2,
                    pos[casa_inicio_andreina][1] - 0.2, pos[casa_inicio_andreina][1] + 0.2],
            zorder=5
        )
        ax.imshow(
            local_icon,
            extent=[pos[destino_ajustado][0] - 0.2, pos[destino_ajustado][0] + 0.2,
                    pos[destino_ajustado][1] - 0.2, pos[destino_ajustado][1] + 0.2],
            zorder=5
        )

        # Dibujar rutas de Javier y Andreína
        ruta_javier = resultados[4]
        ruta_andreina = resultados[5]
        ruta_javier_ajustada = [(n[0] - 50, n[1] - 10) for n in ruta_javier]
        ruta_andreina_ajustada = [(n[0] - 50, n[1] - 10) for n in ruta_andreina]

        if ruta_javier_ajustada:
            nx.draw_networkx_nodes(grafo, pos, nodelist=ruta_javier_ajustada, node_color="#B3E5FC", ax=ax)
            edges_javier = [(ruta_javier_ajustada[i], ruta_javier_ajustada[i + 1]) for i in range(len(ruta_javier_ajustada) - 1)]
            nx.draw_networkx_edges(grafo, pos, edgelist=edges_javier, edge_color="#B3E5FC", width=2, ax=ax)

        if ruta_andreina_ajustada:
            nx.draw_networkx_nodes(grafo, pos, nodelist=ruta_andreina_ajustada, node_color="#FFCDD2", ax=ax)
            edges_andreina = [(ruta_andreina_ajustada[i], ruta_andreina_ajustada[i + 1]) for i in range(len(ruta_andreina_ajustada) - 1)]
            nx.draw_networkx_edges(grafo, pos, edgelist=edges_andreina, edge_color="#FFCDD2", width=2, ax=ax)

        # Agregar etiquetas de calles y carreras en los nodos
        etiquetas = {(x, y): f"C{x+50},Cr{y+10}" for x, y in grafo.nodes() if (x, y) != casa_inicio_andreina and (x, y) != destino_ajustado and (x, y) != casa_inicio_javier}
        nx.draw_networkx_labels(grafo, pos, etiquetas, font_color='black', font_size=6, ax=ax)

        # Agregar etiquetas dentro de los nodos ruta
        #etiquetas = {(x, y): f"C{x+50},Cr{y+10}" for x, y in grafo.nodes() if (x,y) != casa_inicio_andreina and (x, y) != destino_ajustado and (x, y) != casa_inicio_javier and ((x, y) in ruta_javier_ajustada or (x, y) in ruta_andreina_ajustada)}
        #nx.draw_networkx_labels(grafo, pos, etiquetas, font_color='black', font_size=6, ax=ax)

        ax.set_title("Unión de Rutas de Javier y Andreína", fontsize=12)
        ax.axis("off")
        canvas.draw()


# Configuración
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()