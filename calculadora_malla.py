import networkx as nx
import tkinter as tk
import sympy as sp

def construir_grafo(nodos, componentes, conexiones):
    G = nx.Graph()
    for nodo in nodos:
        G.add_node(nodo)
    for c in conexiones:
        if len(c) != 4:
            print(f"Conexión inválida en índice: {c} (esperado 4 elementos)")
            continue
        n1, n2, tipo, valor = c
        G.add_edge(n1, n2, tipo=tipo, valor=valor)
    return G

def detectar_mallas(G, max_mallas=None):
    """
    Detecta la base de ciclos fundamentales del grafo G usando un árbol generador.
    Solo retorna la cantidad mínima de mallas independientes necesarias.
    """
    ciclos = nx.cycle_basis(G)
    E = G.number_of_edges()
    N = G.number_of_nodes()
    L = E - N + 1
    if max_mallas is not None:
        L = min(L, max_mallas)
    return ciclos[:L]


def armar_ecuaciones(mallas, conexiones):
    import sympy as sp

    n = len(mallas)
    I = sp.symbols(f'I1:{n+1}')  # I1, I2, ..., In
    ecuaciones = []
    operaciones = []  # Aquí guardaremos la operación simbólica y numérica

    # Construir un diccionario para guardar TODAS las conexiones entre cada par de nodos
    conn_dict = {}
    for n1, n2, tipo, valor in conexiones:
        key = tuple(sorted([n1, n2]))
        if key not in conn_dict:
            conn_dict[key] = []
        conn_dict[key].append((tipo, valor))

    for idx, malla in enumerate(mallas):
        eq = 0
        suma_resistencias = []
        suma_valores = []
        suma_fuentes = []
        # Recorre los lados de la malla
        for i in range(len(malla)):
            n1 = malla[i]
            n2 = malla[(i+1)%len(malla)]
            key = tuple(sorted([n1, n2]))
            if key in conn_dict:
                for tipo, valor in conn_dict[key]:
                    signo = 1 if (n1 < n2) else -1
                    if tipo == "resistencia":
                        suma_resistencias.append(f"R({n1},{n2})")
                        suma_valores.append(str(valor))
                        suma_corrientes = 0
                        for j, m2 in enumerate(mallas):
                            for k in range(len(m2)):
                                m2_n1 = m2[k]
                                m2_n2 = m2[(k+1)%len(m2)]
                                m2_key = tuple(sorted([m2_n1, m2_n2]))
                                if m2_key == key:
                                    signo_j = 1 if (m2_n1 < m2_n2) else -1
                                    suma_corrientes += I[j] * signo_j
                        eq += valor * suma_corrientes * signo
                    elif tipo == "voltaje":
                        suma_fuentes.append(str(valor))
                        eq -= valor * signo
        ecuaciones.append(eq)
        # Guarda la operación simbólica y numérica
        op_simbolica = " + ".join(suma_resistencias)
        op_numerica = " + ".join(suma_valores)
        op_fuentes = " + ".join(suma_fuentes)
        operaciones.append((op_simbolica, op_numerica, op_fuentes))

    soluciones = sp.solve(ecuaciones, I)
    return ecuaciones, soluciones, operaciones

# Clase para la interfaz gráfica
class Aplicacion:
    def __init__(self, master):
        self.master = master
        master.title("Detector de Mallas")

        self.marco = tk.Frame(master)
        self.marco.pack()

        self.boton_calcular = tk.Button(self.marco, text="Calcular Mallas", command=self.calcular_mallas)
        self.boton_calcular.pack(side=tk.LEFT, padx=5)

    def calcular_mallas(self):
        import calculadora_malla as cm
        import tkinter.simpledialog as sd
        import tkinter.messagebox as mb

        # 1. Detecta nodos manuales
        nodos_manuales = self.obtener_nodos_manuales()
        nodos = [f"N{i}" for i in range(len(nodos_manuales))]
        pos_a_nodo = {pos: nodos[i] for i, pos in enumerate(nodos_manuales)}

        conexiones = []
        conexiones_set = set()

        # 2. Busca componentes entre nodos manuales
        for i, pos1 in enumerate(nodos_manuales):
            for j, pos2 in enumerate(nodos_manuales):
                if i >= j:
                    continue
                # Busca si hay una resistencia, voltaje o cable entre pos1 y pos2 (en línea recta)
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
                                    minvalue=0.01, initialvalue=1.0
                                )
                            if valor is not None:
                                par = tuple(sorted([pos_a_nodo[pos1], pos_a_nodo[pos2]]) + [tipo,valor])
                                if par not in conexiones_set:
                                    conexiones_set.add(par)
                                    conexiones.append((pos_a_nodo[pos1], pos_a_nodo[pos2], tipo, valor))
                        # NO AGREGUES NADA PARA LOS CABLES

        # 3. Construye el grafo y detecta mallas
        import calculadora_malla as cm
        G = cm.construir_grafo(nodos, [], conexiones)
        mallas = cm.detectar_mallas(G, max_mallas=10)
        print("Mallas encontradas:", mallas)
        mb.showinfo("Mallas detectadas", f"{mallas}")
        ecuaciones, soluciones, operaciones = cm.armar_ecuaciones(mallas, conexiones)
        print("Ecuaciones de malla:")
        for eq in ecuaciones:
            print(eq)

        mb.showinfo("Ecuaciones de malla", "\n".join([str(eq) for eq in ecuaciones]))
        print("Soluciones de corrientes de malla:", soluciones)
        mb.showinfo("Solución de mallas", f"{soluciones}")

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

        print("Conexiones detectadas:", conexiones)
