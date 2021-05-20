# Importamos las librerías necesarias
import sys, pygame, pygame.freetype, random
from pygame.locals import *

size = 1600, 900

# Colours    R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
BLACK    = (  0,   0,   0)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (127,   0, 255)
CYAN     = (  0, 255, 255)

class PrimeraEscena:

    def __init__(self, next_scene):
        self.background = pygame.Surface(size)

        self.flechaImg = pygame.image.load('flecha.png')
        self.flechaImg_rect = self.flechaImg.get_rect()
        self.flechaImg_rect = self.flechaImg_rect.move(1300,600)

        self.next_scene = next_scene
        
    def draw(self,screen):
        font = pygame.font.SysFont("comicsansms",90)
        img = font.render('Memory',True, PURPLE)
        screen.blit(img, (620,400)) 
        screen.blit(self.flechaImg, (1300,600))
    
    def update(self, events, dt):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.flechaImg_rect.collidepoint(mouse_pos):
                    return (self.next_scene, None)


class Juego1:
    def __init__(self, next_scene):
        self.background = pygame.Surface(size)
        
        self.images = []
        self.rects = []
        self.imagenes1_array = ['autobus.png','coche.png','barco.png','autobus2.png','grua.png','bici.png']
        for i in self.imagenes1_array:
            self.images.append(pygame.image.load(i))
            s = pygame.Surface((20,20))
            self.rects.append(s.get_rect())

        print(self.images)
        print(self.imagenes1_array)
        

    def start(self, gamestate):
        self.gamestate = gamestate
        for rect in self.rects:
            
            x = random.randint(300,1000)
            y = random.randint(200,700)
            rect.x = x
            rect.y = y
            
        
       
    def draw(self,screen):
        self.background = pygame.Surface(size)
        
        for i in range(len(self.images)):
            #colliding = pygame.Rect.collidelistall(self.rects)
            screen.blit(self.images[i], (self.rects[i].x, self.rects[i].y))
        
    
    def update(self, events, dt):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect in self.rects:
                    if rect.collidepoint(event.pos):
                        print('works!')

def main():
    # Inicializamos pygame
    pygame.init()
    
    # Definimos las dimensiones de la ventana (1600 x 900px) y reloj
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    # Ponemos el título e icono y fondo de la ventana
    pygame.display.set_caption("Quiz Game")
    icon = pygame.image.load('icon.png')
    pygame.display.set_icon(icon)
    fondoImg = pygame.image.load('fondo_memory.png')

    dt = 0
    scenes = {
        'PORTADA': PrimeraEscena('SEGUNDA'),
        'SEGUNDA': Juego1('SEGUNDA'),


    }
    scene = scenes['PORTADA']
    # Comenzamos el bucle del juego
    run=True
    while run:
        # RGB - Red, Green, Blue
        screen.fill ((255,255,255))
        
        # Imagen fondo
        screen.blit(fondoImg, (0,0))

        # Eventos del mouse 
        events = pygame.event.get()

        # Capturamos los eventos que se han producido
        for event in events:
            
            # Definimos eventos:
            if event.type == pygame.QUIT: # Si el evento es salir de la ventana, terminamos
                run = False
            
        result = scene.update(events, dt)
        if result:
            next_scene, state = result
            if next_scene:
                scene = scenes[next_scene]
                scene.start(state)
        scene.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60)
        #pygame.display.update()
   

if __name__ == '__main__':
    main()