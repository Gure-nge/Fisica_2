import tkinter as tk
from collections import defaultdict, deque

TAM_CASILLA = 60
FILA = 8
COLUMNA = 10

def detectar_nodos(componentes):
    grafo = defaultdict(list)
    for (fila, col), tipo in componentes.items():
        if tipo == "cable_h":
            for dcol in [-1, 1]:
                vecino = (fila, col + dcol)
                if vecino in componentes:
                    grafo[(fila, col)].append(vecino)
                    grafo[vecino].append((fila, col))
        elif tipo == "cable_v":
            for dfila in [-1, 1]:
                vecino = (fila + dfila, col)
                if vecino in componentes:
                    grafo[(fila, col)].append(vecino)
                    grafo[vecino].append((fila, col))
    visitados = set()
    nodos = []
    for celda in componentes:
        if celda not in visitados and celda in grafo:
            nodo_actual = []
            cola = deque([celda])
            while cola:
                actual = cola.popleft()
                if actual not in visitados:
                    visitados.add(actual)
                    nodo_actual.append(actual)
                    for vecino in grafo[actual]:
                        if vecino not in visitados:
                            cola.append(vecino)
            nodos.append(nodo_actual)
    print("🔌 Nodos detectados:")
    for i, grupo in enumerate(nodos):
        print(f" Nodo {i}: {grupo}")
    return nodos

class CircuitEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Circuitos")

        self.canvas = tk.Canvas(root, width=COLUMNA * TAM_CASILLA, height=FILA * TAM_CASILLA, bg="white")
        self.canvas.pack()

        self.componentes = {}  # clave: (fila, col), valor: tipo
        self.componente_seleccionado = "resistencia"

        self.dibujar_rejilla()
        self.crear_botones()
        self.canvas.bind("<Button-1>", self.colocar_componente)

    def dibujar_rejilla(self):
        for i in range(FILA):
            for j in range(COLUMNA):
                x0 = j * TAM_CASILLA
                y0 = i * TAM_CASILLA
                x1 = x0 + TAM_CASILLA
                y1 = y0 + TAM_CASILLA
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="lightgray")

    def crear_botones(self):
        marco = tk.Frame(self.root)
        marco.pack(pady=5)

        botones = [
            ("Resistencia", "resistencia"),
            ("Voltaje", "voltaje"),
            ("Cable H", "cable_h"),
            ("Cable V", "cable_v"),
            ("Nodo", "nodo")
        ]

        for texto, tipo in botones:
            b = tk.Button(marco, text=texto, command=lambda t=tipo: self.seleccionar_componente(t))
            b.pack(side=tk.LEFT, padx=5)

        tk.Button(marco, text="Detectar Nodos", command=self.mostrar_nodos).pack(side=tk.LEFT, padx=5)

    def mostrar_nodos(self):
        nodos = detectar_nodos(self.componentes)
        self.canvas.delete("nodo_id")  # Borra círculos anteriores

        # Dibuja los nodos detectados y los etiqueta
        for i, grupo in enumerate(nodos):
            for (fila, col) in grupo:
                x = col * TAM_CASILLA + TAM_CASILLA // 2
                y = fila * TAM_CASILLA + TAM_CASILLA // 2
                r = 6  # radio del nodo visual
                self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="blue", outline="black", tags="nodo_id")
                self.canvas.create_text(x + 10, y - 10, text=f"N{i}", fill="blue", font=("Arial", 8), tags="nodo_id")

    def seleccionar_componente(self, tipo):
        self.componente_seleccionado = tipo

    def colocar_componente(self, evento):
        col = evento.x // TAM_CASILLA
        fila = evento.y // TAM_CASILLA
        pos = (fila, col)

        if pos in self.componentes:
            self.componentes.pop(pos)
        else:
            self.componentes[pos] = self.componente_seleccionado

        self.redibujar_componentes()

    def redibujar_componentes(self):
        self.canvas.delete("componente")
        for (fila, col), tipo in self.componentes.items():
            x = col * TAM_CASILLA + TAM_CASILLA // 2
            y = fila * TAM_CASILLA + TAM_CASILLA // 2

            if tipo == "resistencia":
                self.canvas.create_rectangle(x-20, y-10, x+20, y+10, fill="orange", tags="componente")
                self.canvas.create_text(x, y, text="R", tags="componente")
            elif tipo == "voltaje":
                self.canvas.create_oval(x-15, y-15, x+15, y+15, outline="blue", width=2, tags="componente")
                self.canvas.create_text(x, y, text="V", tags="componente")
            elif tipo == "cable_h":
                self.canvas.create_line(x-20, y, x+20, y, fill="black", width=3, tags="componente")
            elif tipo == "cable_v":
                self.canvas.create_line(x, y-20, x, y+20, fill="black", width=3, tags="componente")
            elif tipo == "nodo":
                r = 6
                self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="blue", outline="black", tags="componente")

    def calcular_mallas(self):
        # Extrae nodos y conexiones del circuito dibujado
        # Nodos: todos los nodos detectados
        # Conexiones: cada componente entre dos nodos
        nodos_detectados = detectar_nodos(self.componentes)
        nodos = [f"N{i}" for i in range(len(nodos_detectados))]
        conexiones = []

        # Mapea cada celda a su nodo
        celda_a_nodo = {}
        for idx, grupo in enumerate(nodos_detectados):
            for celda in grupo:
                celda_a_nodo[celda] = f"N{idx}"

        # Busca conexiones entre nodos (solo resistencias y voltajes)
        for (fila, col), tipo in self.componentes.items():
            if tipo in ("resistencia", "voltaje"):
                # Busca vecinos conectados por cables
                for df, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    vecino = (fila+df, col+dc)
                    if vecino in celda_a_nodo and (fila, col) in celda_a_nodo:
                        n1 = celda_a_nodo[(fila, col)]
                        n2 = celda_a_nodo[vecino]
                        if n1 != n2:
                            # Valor por defecto (puedes pedirlo al usuario)
                            valor = 1.0
                            conexiones.append((n1, n2, tipo, valor))

        # Importa y usa calculadora_malla
        import calculadora_malla as cm
        G = cm.construir_grafo(nodos, [], conexiones)
        mallas = cm.detectar_mallas(G)
        print("Mallas encontradas:", mallas)
        # Aquí podrías mostrar las mallas en la interfaz o resolverlas

        # (Opcional) Mostrar en un messagebox
        import tkinter.messagebox as mb
        mb.showinfo("Mallas detectadas", f"{mallas}")


