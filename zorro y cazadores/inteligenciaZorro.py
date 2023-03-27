import networkx as nx
import matplotlib.pyplot as plt

class IA_Zorro:
    
    #_ espacio no disponibles
    #X posicion bloqueada
    def __init__(self, profundidad):
        self.tablero = [['X', '-', 'X', '-', 'X', '-', 'X', '-'],
                        ['-', 'X', '-', 'X', '-', 'X', '-', 'X'],
                        ['X', '-', 'X', '-', 'X', '-', 'X', '-'],
                        ['-', 'X', '-', 'X', '-', 'X', '-', 'X'],
                        ['X', '-', 'X', '-', 'X', '-', 'X', '-'],
                        ['-', 'X', '-', 'X', '-', 'X', '-', 'X'],
                        ['X', '-', 'X', '-', 'X', '-', 'X', '-'],
                        ['-', 'X', '-', 'X', '-', 'X', '-', 'X']]
        #(fila, columna)
        self.movimientos_cazadores = [(-1, 1), (-1, -1)]
        self.movimientos_zorro = [(-1, 1), (1, 1), (-1,-1),(1,-1)]
        self.profundidad = profundidad #ramificaciones a evaluar
        #se crean los nodos y aristas que representan las relaciones del tablero y se almacena en una variable global para la clase
        self.grafo = self.aristasGrafo(self.tablero, self.nodosGrafo(self.tablero))

    #Evalua todas las posiciones para saber si la coordenada ingresada es valida
    def es_posicion_valida(self, posicion, posicion_zorro, cazadores_posiciones):
        fila, columna = posicion #coordenada
        #si la coodenada en la fila es valida
        if fila < 0 or fila >= len(self.tablero):
            return False
        #si la cooredenada en la columna es valida 
        if columna < 0 or columna >= len(self.tablero[0]):
            return False
        #si el camino no esta bloqeuado
        if self.tablero[fila][columna] == 'X':
            return False
        #si la casilla no esta ocupada por un cazador
        for cazador_posicion in cazadores_posiciones:
            if posicion == cazador_posicion:
                return False
        #si la casilla no esta ocpuada por el zorro
        if posicion == posicion_zorro:
                return False
        return True

    def nodosGrafo(self, tablero):
        grafo = nx.Graph()
        #se añade los nodos al grafo
        for fila in range(len(tablero)):#recorrido para las filas 
            for columna in range(len(tablero[fila])):#recorido para las columnas (cada elemento de la fila)
                #si no es cazador ni un cuadro bloquedo (casillas blancas), es un nodo valido 
                if tablero[fila][columna] != 'X' and tablero[fila][columna] != 'C': 
                    #se agregan los nodos al grafo
                    grafo.add_node((fila,columna))
        return grafo
    
    def aristasGrafo(self, tablero, grafo):
        # se añade las aristas al grafo (vertices)
        for fila in range(len(tablero)): #recorrido de las filas
            for columna in range(len(tablero[fila])): #recorido para las columnas (cada elemento de la fila)
                #si la posicion no esta bloqueada, ni es un cazador
                if tablero[fila][columna] != 'X' and tablero[fila][columna] != 'C':
                    neighbors = []
                    #se evalua que no se encuentra en el borde superior ni en el borde izquierdo
                    #y se evelua la posicion abajo a la izquierda esta libre o es el zorro
                    if fila > 0 and columna > 0 and (tablero[fila-1][columna-1] == '-' or tablero[fila-1][columna-1] == 'Z'):
                        neighbors.append((fila-1, columna-1))
                    #se evalua que no se encuentra en el borde superior ni en el borde derecho
                    #y se evalua la posicio arriba a la izquierda esta libre o es el zorro
                    if fila > 0 and columna < len(tablero[0])-1 and (tablero[fila-1][columna+1] == '-' or tablero[fila-1][columna+1] == 'Z'):
                        neighbors.append((fila-1, columna+1))
                    #se evalua que no se encuentra en el borde inferior ni en el borde izquierdo
                    #y se evalua la posicio abajo a la derecha esta libre o es el zorro
                    if fila < len(tablero)-1 and columna > 0 and (tablero[fila+1][columna-1] == '-' or tablero[fila+1][columna-1] == 'Z'):
                        neighbors.append((fila+1, columna-1))
                    #se evalua que no se encuentra en la última fila ni en la última columna de la tabla
                    #y se evalua la posicio arriba a la derecha esta libre o es el zorro
                    if fila < len(tablero)-1 and columna < len(tablero[0])-1 and (tablero[fila+1][columna+1] == '-' or tablero[fila+1][columna+1] == 'Z'):
                        neighbors.append((fila+1, columna+1))
                    for neighbor in neighbors:
                        #se agregan los vertices al nodo
                        grafo.add_edge((fila,columna), neighbor, weight=1)
        return grafo

    #Retorna las filas mas cercanas a las metas, validas para calcular las rutas
    def posiblesMetas(self, grafo, zorro_posicion):
        #grafo.nodes() contiene una lista de nodos, que son almacenados en una lista simple para realizar recorridos con el indice
        listaNodos = list(grafo.nodes())
        nodosLejanos = []
        try: #arrojara error si el grafo esta vacio
            contador = 0
            #recorre los elementos en orden inverso (las ultimas posiciones son las mas alejadas y las que interesa evaluar)
            bandera = True
            for meta in reversed(listaNodos):
                #si exite una ruta valida entre el ultimo nodo y la posicion del zorro
                if nx.has_path(grafo, zorro_posicion, meta):
                    if bandera: # si es primer nodo valido, se almacena le nivel de la fila
                        filaLejana = meta[0]#posicion mas lejana y accesible (posible meta)
                        bandera = False
                        nodosLejanos.append(meta)
                    elif filaLejana == meta[0]: #si pertenece a la misma fila que el nodomas lejano
                        nodosLejanos.append(meta)
                    else:#si no significa, que ya no hay mas elementos de la misma fila a los cuales se puedan acceder
                        break
        except TypeError as error:
            print(error)
        return nodosLejanos

    #retorna las distintas rutas posibles, para cada posible meta
    def distanciasCortas(self, grafo, posicionZorro, posiblesMeta): 
        source = tuple(posicionZorro)
        resultado = []
        #para cada posible meta
        for meta in posiblesMeta:
            target = tuple(meta)
            # se obtiene la ruta más corta utilizando el algoritmo de Dijkstra
            resultado.append(nx.dijkstra_path(grafo, source, target))
        return resultado
    
    #retorna una de las rutas mas corta de entre las distintas rutas posibles (maximo 4)
    def distanciaCorta(self, rutas):
        corta = rutas[0]
        for ruta in rutas:
            if len(ruta)<len(corta):
                corta = ruta
        return corta
    
    # funcion que permite determinar quien tiene mas ventaja, basado en que tan cerca, esta el zorro de llegar al otro lado del tablero
    # tomando en cuenta que no puede ir por las X, y que los casadores tambien impiden el paso, a medida que se van desplazando
    def grafoCazador(self, grafo, cazadores_posiciones):
        nuevoGrafo = grafo.copy() #crea un nuevo grafo para no modigicar el anterior
        for cazador in cazadores_posiciones:
            nuevoGrafo.remove_node(cazador) #se eliminan los nodos donde estan los cazadors
        return nuevoGrafo

    def valuar_tablero(self, zorro_posicion, cazadores_posiciones):
        puntaje = 0
        #si la posicion es la meta, se le da una recompenza muy alta para que elija esa opcion por sobre todas las demas
        if self.es_estado_final(zorro_posicion):
            puntaje += 10000000
        #Penalizar si el zorro está en una fila antes de la fila 8
        if zorro_posicion[0] < 7:
            puntaje -= 1000
        #mientras mas lejos este de la ultima fila menos punto recibira
        puntaje = puntaje - (100*(7-zorro_posicion[0]))
        #Puntaje basado en la ruta mas corta
        #cuantas casillas tiene que recorrer, en la ruta mas corta para llegar a la meta,
        #mientras mas distancia tenga que recorrer mayor sera la penalizacion
        grafoCazador = self.grafoCazador(self.grafo, cazadores_posiciones)#grafo que toma en cuenta la poscicion de los cazadores
        #numero de pasos que posee la ruta mas cota entre el zorro y la posible meta
        distancia_zorro = len(self.distanciaCorta(self.distanciasCortas( grafoCazador, zorro_posicion, self.posiblesMetas(grafoCazador, zorro_posicion))))
        puntaje = puntaje -(4*distancia_zorro)
        #mientras se encuentre mas alejado de los cazadores mejor
        distancias = []
        for cazador in cazadores_posiciones:
            distancia_horizontal = abs(cazador[1] - zorro_posicion[1])
            distancia_vertical = abs(cazador[0] - zorro_posicion[0])
            distancia_maxima = max(distancia_horizontal, distancia_vertical)
            distancias.append(distancia_maxima)
            #utiliza la coordenad mas alejada como referencia y la agrega a una lista

        distancia_cazadores = sum(distancias)#suma todas las distancas con respecto a cada cazador
        puntaje = puntaje + (2*distancia_cazadores)#mientras mas alejado este recibe mejor puntuacion

        return puntaje
    
    #si se llega a la meta
    def es_estado_final(self, zorro_posicion):
        metas = [(7,0), (7, 2), (7, 4), (7, 6)]
        for meta in metas:
            if zorro_posicion == meta:
                return True
        return False
    
    #genera las posibles jugadas del zorro en coordenadas validas
    def obtener_movimientos_zorro(self, zorro_posicion, cazadores_posiciones):
        resultado = []
        for movimiento in self.movimientos_zorro:
            fila, columna = movimiento
            fila = fila + zorro_posicion[0]
            columna = columna + zorro_posicion[1]
            if self.es_posicion_valida((fila, columna), zorro_posicion, cazadores_posiciones):
                resultado.append((fila, columna))
        return resultado
    
    #modificar una posicion de uno de los cazadores de entre 4 cazadores
    def remplazar_posicion_cazador(self, indice, posicion, cazadores_posiciones):
        contador = 0
        resultado = []
        for cazador in cazadores_posiciones:
            if contador == indice:
                resultado.append(posicion)
            else:
                resultado.append(cazador)
            contador += 1
        return resultado

    #genera todas las posibles combinatorias de jugadas validas por realizar los cazadores
    def obtener_movimientos_cazador(self, zorro_posicion, cazadores_posiciones):
        resultado = []
        #Para cada posible movimiento de los cazadores
        for movimiento in self.movimientos_cazadores:
            #se evalua cada cazador
            indice = 0
            for cazador in cazadores_posiciones:
                #movimiento contiene dos coordenadas
                fila, columna = movimiento
                #en la fila y en la columna se modifican los indices segun los movimientos que pudieran relizar el cazador
                fila = fila + cazador[0] 
                columna = columna + cazador[1]
                if self.es_posicion_valida((fila, columna), zorro_posicion, cazadores_posiciones):
                    #se el movimiento es valido, se almacena
                    resultado.append(self.remplazar_posicion_cazador(indice, (fila, columna), cazadores_posiciones))
                indice += 1
        return resultado
    
    def minimax(self, profundidad, es_maximizador, zorro_posicion, cazadores_posiciones):
        # Evaluar el tablero si se alcanza la profundidad máxima o si es un estado final
        if profundidad == 0 or self.es_estado_final(zorro_posicion):
            return self.valuar_tablero(zorro_posicion, cazadores_posiciones)
        
        # Maximizador al ventaja del zorro
        if es_maximizador:
            max_evaluacion = float('-inf')
            movimientos_zorro = self.obtener_movimientos_zorro(zorro_posicion, cazadores_posiciones)   
            #evaluar para cada posible movimiento del zorro
            for movimiento in movimientos_zorro:
                evaluacion = self.minimax(profundidad - 1, False, movimiento, cazadores_posiciones)
                #se almacena la jugada que retorne mayor beneficio
                max_evaluacion = max(max_evaluacion, evaluacion)
            return max_evaluacion
        
        # Minimizador la ventaja de los cazadores
        else:
            min_evaluacion = float('inf')
            movimientos_cazadores = self.obtener_movimientos_cazador(zorro_posicion, cazadores_posiciones)
            #para cada posible combinatoria de jugada de los cazadores            
            for movimiento in movimientos_cazadores:
                evaluacion = self.minimax(profundidad - 1, True, zorro_posicion, movimiento)
                min_evaluacion = min(min_evaluacion, evaluacion) #se elije la jugade que le de menos ventaja
            return min_evaluacion
    
    def mejor_jugada(self, zorro_posicion, cazadores_posiciones):
        movimientos_zorro = self.obtener_movimientos_zorro(zorro_posicion, cazadores_posiciones)

        contador = 0
        for movimiento in movimientos_zorro:

            if contador == 0:
                #almaceno el primer movimiento, y el valor que este arroja
                mejor_movimeinto = movimiento
                valor_max = self.minimax(self.profundidad, True, movimiento, cazadores_posiciones)
            else:
                valor_jugada = self.minimax(self.profundidad, True, movimiento, cazadores_posiciones)
                #si existe una jugada con mejor valoracion
                if valor_max < valor_jugada:
                    mejor_movimeinto = movimiento
                    valor_max = valor_jugada
            contador += 1

        return mejor_movimeinto

    # def show(self):
    #     nx.draw(self.grafo, with_labels=True)
    #     plt.show()