import tkinter as tk

TAM_CASILLA = 60
FILA = 10
COLUMNA = 10

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

        tk.Button(marco, text="Calcular Mallas", command=self.calcular_mallas).pack(side=tk.LEFT, padx=5)

    def seleccionar_componente(self, tipo):
        self.componente_seleccionado = tipo

    def colocar_componente(self, evento):
        import tkinter.simpledialog as sd

        col = evento.x // TAM_CASILLA
        fila = evento.y // TAM_CASILLA
        pos = (fila, col)

        if pos in self.componentes:
            self.componentes.pop(pos)
        else:
            tipo = self.componente_seleccionado
            valor = None
            if tipo in ("resistencia", "voltaje"):
                valor = sd.askfloat(
                    "Valor del componente",
                    f"Ingrese el valor para {tipo.upper()} en ({fila},{col}):",
                    initialvalue=1.0
                )
                if valor is None:
                    return  # No colocar si el usuario cancela
                self.componentes[pos] = (tipo, valor)
            else:
                self.componentes[pos] = tipo

        self.redibujar_componentes()
        
    def redibujar_componentes(self):
        self.canvas.delete("componente")
        # --- Primero, obtenemos los nodos manuales y les asignamos un número ---
        nodos_manuales = []
        for (fila, col), dato in self.componentes.items():
            tipo = dato[0] if isinstance(dato, tuple) else dato
            if tipo == "nodo":
                nodos_manuales.append((fila, col))
        pos_a_nodo = {pos: f"N{i}" for i, pos in enumerate(nodos_manuales)}
        # --- Ahora dibujamos todos los componentes ---
        for (fila, col), dato in self.componentes.items():
            if isinstance(dato, tuple):
                tipo, valor = dato
            else:
                tipo = dato
                valor = None

            x = col * TAM_CASILLA + TAM_CASILLA // 2
            y = fila * TAM_CASILLA + TAM_CASILLA // 2

            if tipo == "resistencia":
                self.canvas.create_rectangle(x-20, y-10, x+20, y+10, fill="orange", tags="componente")
                self.canvas.create_text(x, y, text=f"R\n{valor}", tags="componente")
            elif tipo == "voltaje":
                self.canvas.create_oval(x-15, y-15, x+15, y+15, outline="blue", width=2, tags="componente")
                self.canvas.create_text(x, y, text=f"V\n{valor}", tags="componente")
            elif tipo == "cable_h":
                self.canvas.create_line(x-20, y, x+20, y, fill="black", width=3, tags="componente")
            elif tipo == "cable_v":
                self.canvas.create_line(x, y-20, x, y+20, fill="black", width=3, tags="componente")
            elif tipo == "nodo":
                r = 6
                self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="blue", outline="black", tags="componente")
                # Dibuja el número del nodo al lado del punto azul
                nombre_nodo = pos_a_nodo.get((fila, col), "")
                self.canvas.create_text(x, y-15, text=nombre_nodo, fill="black", font=("Arial", 10, "bold"), tags="componente")

    def calcular_mallas(self):
        import calculadora_malla as cm
        import tkinter.simpledialog as sd
        import tkinter.messagebox as mb

        # 1. Detecta nodos manuales
        nodos_manuales = self.obtener_nodos_manuales()
        if len(nodos_manuales) < 2:
            mb.showerror("Error", "Debes colocar al menos dos nodos manuales para analizar mallas.")
            return

        nodos = [f"N{i}" for i in range(len(nodos_manuales))]
        pos_a_nodo = {pos: nodos[i] for i, pos in enumerate(nodos_manuales)}

        conexiones = []
        conexiones_set = set()

        # 2. Busca componentes entre nodos manuales (en línea recta)
        for i, pos1 in enumerate(nodos_manuales):
            for j, pos2 in enumerate(nodos_manuales):
                if i >= j:
                    continue
                camino = self.obtener_camino(pos1, pos2)
                if not camino:
                    continue
                # Busca si hay un componente entre los nodos
                for punto in camino:
                    if punto in self.componentes:
                        dato = self.componentes[punto]
                        tipo = dato[0] if isinstance(dato, tuple) else dato
                        valor = dato[1] if isinstance(dato, tuple) else None
                        if tipo in ("resistencia", "voltaje"):
                            if valor is None:
                                valor = sd.askfloat(
                                    "Valor del componente",
                                    f"Ingrese el valor para {tipo.upper()} entre {pos1} y {pos2}:",
                                    initialvalue=1.0
                                )
                            par = tuple(sorted([pos_a_nodo[pos1], pos_a_nodo[pos2]]) + [tipo, valor, punto])
                            if par not in conexiones_set:
                                conexiones_set.add(par)
                                conexiones.append((pos_a_nodo[pos1], pos_a_nodo[pos2], tipo, valor))
                        elif tipo in ("cable_h", "cable_v"):
                            # Si solo hay cables, puedes poner una resistencia de valor 0 (o 1e-6)
                            par = tuple(sorted([pos_a_nodo[pos1], pos_a_nodo[pos2]]) + ["resistencia", 1e-6])
                            if par not in conexiones_set:
                                conexiones_set.add(par)
                                conexiones.append((pos_a_nodo[pos1], pos_a_nodo[pos2], "resistencia", 1e-6))
                        # Si quieres que los capacitores participen en el análisis, agrega aquí la lógica

        # 3. Construye el grafo y detecta mallas
        G = cm.construir_grafo(nodos, [], conexiones)
        mallas = cm.detectar_mallas(G, max_mallas=10)
        print("Mallas encontradas:", mallas)
        mb.showinfo("Mallas detectadas", f"{mallas}")
        ecuaciones, soluciones, operaciones = cm.armar_ecuaciones(mallas, conexiones)
        msg = ""
        for idx, (op_simbolica, op_numerica, op_fuentes) in enumerate(operaciones):
            msg += f"Malla {idx+1}:\n"
            if op_simbolica:
                msg += f"  Operación simbólica: {op_simbolica}\n"
                msg += f"  Operación numérica: {op_numerica}\n"
            if op_fuentes:
                msg += f"  Fuentes: {op_fuentes}\n"
            msg += f"  Ecuación: {ecuaciones[idx]}\n\n"

        import tkinter.messagebox as mb
        mb.showinfo("Operación de malla(s)", msg)
        mb.showinfo("Solución de mallas", f"{soluciones}")

        self.canvas.delete("flecha_malla")  # Borra flechas anteriores

        for malla in mallas:
            for i in range(len(malla)):
                n1 = malla[i]
                n2 = malla[(i+1)%len(malla)]
                pos1 = pos2 = None
                for pos, nombre in pos_a_nodo.items():
                    if nombre == n1:
                        pos1 = pos
                    if nombre == n2:
                        pos2 = pos
                if pos1 and pos2:
                    x0 = pos1[1] * TAM_CASILLA + TAM_CASILLA // 2
                    y0 = pos1[0] * TAM_CASILLA + TAM_CASILLA // 2
                    x1 = pos2[1] * TAM_CASILLA + TAM_CASILLA // 2
                    y1 = pos2[0] * TAM_CASILLA + TAM_CASILLA // 2
                    self.dibujar_flecha_pequena(x0, y0, x1, y1)

    def obtener_nodos_manuales(self):
        nodos_manuales = []
        for (fila, col), dato in self.componentes.items():
            tipo = dato[0] if isinstance(dato, tuple) else dato
            if tipo == "nodo":
                nodos_manuales.append((fila, col))
        return nodos_manuales

    def obtener_camino(self, pos1, pos2):
        # Solo permite caminos horizontales o verticales
        fila1, col1 = pos1
        fila2, col2 = pos2
        camino = []
        if fila1 == fila2:
            # Horizontal
            for c in range(min(col1, col2)+1, max(col1, col2)):
                camino.append((fila1, c))
        elif col1 == col2:
            # Vertical
            for f in range(min(fila1, fila2)+1, max(fila1, fila2)):
                camino.append((f, col1))
        else:
            return None  # No es un camino recto
        return camino

    def dibujar_flecha(self, x0, y0, x1, y1, color="red"):
        self.canvas.create_line(x0, y0, x1, y1, arrow=tk.LAST, fill=color, width=2, tags="flecha_malla")

    def dibujar_flecha_pequena(self, x0, y0, x1, y1, color="red"):
        # Calcula el punto medio
        xm = (x0 + x1) / 2
        ym = (y0 + y1) / 2
        # Calcula la dirección
        dx = x1 - x0
        dy = y1 - y0
        longitud = (dx**2 + dy**2) ** 0.5
        if longitud == 0:
            return
        # Normaliza y escala la flecha
        escala = 24
        ux = dx / longitud
        uy = dy / longitud
        # Perpendicular para desplazar la flecha
        perp_x = -uy
        perp_y = ux
        desplazamiento = 18  # píxeles fuera de la línea
        xm_d = xm + perp_x * desplazamiento
        ym_d = ym + perp_y * desplazamiento
        # Punto de la punta
        px = xm_d + ux * escala / 2
        py = ym_d + uy * escala / 2
        # Base de la flecha
        bx = xm_d - ux * escala / 2
        by = ym_d - uy * escala / 2
        # Alas
        wing = 7
        # Dibuja la línea central
        self.canvas.create_line(bx, by, px, py, fill=color, width=3, tags="flecha_malla")
        # Dibuja las alas
        self.canvas.create_line(px, py, px - ux * 7 + perp_x * wing, py - uy * 7 + perp_y * wing, fill=color, width=3, tags="flecha_malla")
        self.canvas.create_line(px, py, px - ux * 7 - perp_x * wing, py - uy * 7 - perp_y * wing, fill=color, width=3, tags="flecha_malla")


