import pygame,sys
from inteligenciaZorro import IA_Zorro
from pygame.locals import *

# Definir una clase para el tablero
class Board:
    def __init__(self, screen):
        # Crear una matriz de 8x8 para representar el tablero
        self.board = [[0 for j in range(8)] for i in range(8)]
        # Empezar sin haber selecionado ningun hunter
        self.selected_hunter = None
        self.screen = screen
        # Crear cuatro piezas de cazadores con sus posiciones iniciales en el tablero
        self.hunters = [
            Hunter(7, 0, self.screen),
            Hunter(7, 2, self.screen),
            Hunter(7, 4, self.screen),
            Hunter(7, 6, self.screen)
        ]
        self.zorro = Zorro(0, 3, self.screen) # se crea la pieza del zorro con su posicion inicia en el tablero
        #inteligencia artificial para movel al zorro
        self.IA_zorro = IA_Zorro(3)

    # Definir una función para dibujar el tablero
    def draw_board(self):
        for i in range(8):
            for j in range(8):
                # Alternar colores de las casillas
                color = (255, 255, 255) if (i + j) % 2 == 0 else (0, 0, 0)
                pygame.draw.rect(self.screen, color, (j * (75), i * 75, 75, 75))

    # Manejar eventos de Pygame
    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #si solicitan cerrar la ventana
                pygame.quit()
                sys.exit() #se cierra el programa
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Obtener la posición del click
                x, y = pygame.mouse.get_pos()
                # Convertir la posición en una casilla de la cuadrícula
                x //= 75
                y //= 75
                # Si no se ha seleccionado una pieza de cazador, buscar una pieza de cazador en esa casilla
                if self.selected_hunter is None:
                    for hunter in self.hunters:
                        if hunter.x == x and hunter.y == y:
                            self.selected_hunter = hunter
                            break
                # Si ya se ha seleccionado una pieza de cazador, moverla a la casilla seleccionada
                elif self.selected_hunter is not None:
                    if self.selected_hunter.move(x, y,self.hunters):
                        #si la jugada es valida, tambien debe de jugar el zorro
                        if self.jugar_zorro() == False:
                            ventana2 = Ventana(230, 200)
                            ventana2.form("YOU WIN!!")
                            ventana2.mostrar_ventana_aviso()
                    self.selected_hunter = None

    #retorna la posicion de los cazadores en un formato que la ia entiende
    def get_hunters(self):
        resultado = []
        for hunter in self.hunters:
            resultado.append(hunter.get_posicion())
        return resultado
    
    def jugar_zorro(self):
        try: #en caso de no haber jugada posible arrojara error dado que intentarar moverse a una casilla que no existe
             #al estar ocupada por un cazador se elimina de la representacion del entorno por donde puede trancitar
            #print( self.get_hunters())
            jugadaFila, jugadaColumna = self.IA_zorro.mejor_jugada(self.zorro.get_posicion(), self.get_hunters())
            self.zorro.move(jugadaFila, jugadaColumna, self.hunters)
            
            return True
        except:
            return False

    # Actualizar la pantalla
    def update_screen(self):
        # Dibujar el tablero
        self.draw_board()
        # Dibujar los cazadores
        for hunter in self.hunters:
            hunter.draw_hunter()
        self.zorro.draw_zorro()
        if self.IA_zorro.es_estado_final(self.zorro.get_posicion()):
            ventana = Ventana(230,200)
            ventana.form("YOU LOSE")
            ventana.mostrar_ventana_aviso()
        pygame.display.flip()


# Definir una clase para el hunter
class Hunter:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.image = pygame.image.load('hunter.png')
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.screen = screen

    def casilla_ocupada(self, x, y, hunters):
        for hunter in hunters:
            if hunter.x == x and hunter.y == y:
                return True
        return False

    def draw_hunter(self):
        # Dibujar imagen de cazador en la posición actual
        self.screen.blit(self.image, (self.x * 75, self.y * 75))

    def move(self, x, y, hunters):
        # Verificar que la nueva posición está en una casilla negra
        #si es impar
        if (x + y) % 2 != 0:
            #comprobar adyacencia en horizontal
            if abs(x - self.x) <= 1:
                #comprobar adyacencia en vertical
                if abs(y - self.y) <= 1:
                    #la nueva coordenada en y es menor que la actual
                    if x < self.x:
                        if self.casilla_ocupada(x, y, hunters):
                            return False #para saber que la modificacion no fue valida
                        else:
                            self.x = x
                            self.y = y
                            return True #para saber qeu si se realizao un movimiento
                    
    def get_posicion(self):
        return (self.x , self.y)

# Definir una clase para el zorro
class Zorro:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.image = pygame.image.load('zorro.png')
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.screen = screen
    def casilla_ocupada(self, x, y, hunters):
        for hunter in hunters:
            if hunter.x == x and hunter.y == y:
                return True
        return False

    def draw_zorro(self):
        # Dibujar imagen de cazador en la posición actual
        self.screen.blit(self.image, (self.x * 75, self.y * 75))

    def move(self, x, y, hunters):
        # Verificar que la nueva posición está en una casilla negra
        if self.casilla_ocupada(x, y, hunters):
            pass
        else:
            self.x = x
            self.y = y
            
    def get_posicion(self):
        return (self.x , self.y)

class Ventana:

    def __init__(self, ancho, alto):
        pygame.init()
        self.ancho = ancho
        self.alto = alto
        self.screen = pygame.display.set_mode((self.ancho, self.alto))

    def getSize(self):
        return (self.ancho,self.alto)

    def form(self, texto):
        self.fuente = pygame.font.Font(None, 40)
        self.texto_perdiste = self.fuente.render(texto, True, (255, 255, 255))
        self.texto_volver = self.fuente.render("Volver a intentar", True, (255, 255, 255))
        self.rect_perdiste = self.texto_perdiste.get_rect(center=(self.ancho / 2, self.alto / 2 - 50))
        self.rect_volver = self.texto_volver.get_rect(center=(self.ancho / 2, self.alto / 2 + 50))

    def mostrar_ventana_aviso(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect_volver.collidepoint(event.pos):
                        self.screen = pygame.display.set_mode((600,600))
                        main()
                        
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.texto_perdiste, self.rect_perdiste)
            pygame.draw.rect(self.screen, (255, 255, 255), self.rect_volver, 2)
            self.screen.blit(self.texto_volver, self.rect_volver)
            pygame.display.update()


def main():
    VentanaPrincipal = Ventana(600,600)
    screen = VentanaPrincipal.screen
    tablero = Board(screen)
    running = True
    # Ciclo principal del juego
    while running:
        #Manejar eventos del tablero
        tablero.handle_event()
        #Actualizar la pantalla
        tablero.update_screen()
    # Salir de Pygame
    pygame.quit()

if __name__ == '__main__':
    main()

