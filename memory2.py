# Import libraries
import sys, pygame, pygame.freetype, random
from pygame.locals import *

# Set size of window
size = 1280,768
background_img = pygame.image.load('fondo_memory.png')

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

# PORTRAIT SCENE
class PORTRAIT:

    def __init__(self, next_scene):
        # Initialize variables
        self.background = pygame.Surface(size)

        self.flechaImg = pygame.image.load('flecha.png')
        self.flechaImg_rect = self.flechaImg.get_rect()
        self.flechaImg_rect = self.flechaImg_rect.move(1000,500)

        self.next_scene = next_scene
        
    def draw(self,screen):
        # Draw them 
        font = pygame.font.SysFont("comicsansms",80)
        img = font.render('Memory',True, PURPLE)
        screen.blit(img, (500,334)) 
        screen.blit(self.flechaImg, (1000,500))
    
    def update(self, events, dt):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.flechaImg_rect.collidepoint(mouse_pos):
                    return (self.next_scene, None)


class GAME1:
    def __init__(self, next_scene):
        self.background = pygame.Surface(size)
        
        # Create an array of images with their rect
        self.images = []
        self.rects = []
        self.imagenes1_array = ['autobus.png','coche.png','barco.png','autobus2.png','grua.png','bici.png']
        
        for i in self.imagenes1_array:
            # We divide in variables so we can then get the rect of the whole Img (i2)
            i2 = pygame.image.load(i)
            self.images.append(i2)
            s = pygame.Surface(i2.get_size())
            r = s.get_rect()
            
            # Trying to use colliderect so it doesnt overlap
            position_set = False 
            while not position_set:
                r.x = random.randint(200,840)
                r.y = random.randint(100,600)    

                margin = 10
                rl = [rect.inflate(margin*2, margin*2) for rect in self.rects]
                if len(self.rects) == 0 or r.collidelist(rl) < 0:
                    self.rects.append(r)
                    position_set = True
    
        print(self.images)

    def start(self, gamestate):
        self.gamestate = gamestate
       
    def draw(self,screen):
        self.background = pygame.Surface(size)
        font = pygame.font.SysFont("comicsansms",60)
        
        # First half 
        text1 = font.render('¡A recordar!',True, PURPLE)
        # Show image to remember and then fade out
        coche_img = pygame.image.load('coche.png')
        #screen.blit(coche_img, (600, 450))
        text1_1 = text1.copy()
        # This surface is used to adjust the alpha of the txt_surf.
        alpha_surf = pygame.Surface(text1_1.get_size(), pygame.SRCALPHA)
        alpha = 255 # The current alpha value of the surface.

        if alpha > 0:
            alpha = max(alpha-4, 0)
            text1_1 = text1.copy()
            alpha_surf.fill((255, 255, 255, alpha))
            text1_1.blit(alpha_surf, (0,0), special_flags = pygame.BLEND_RGBA_MULT)
        
        screen.blit(text1_1, (500,30))
       

        # Second half (Show all similar images)
        text2 = font.render('¿Cuál era el dibujo?',True, PURPLE)
        #screen.blit(text2, (500,50))
        
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
    pygame.display.set_caption("Memory")
    icon = pygame.image.load('icon.png')
    pygame.display.set_icon(icon)
    fondoImg = pygame.image.load('fondo_memory.png')

    # Setting up Scenes
    dt = 0
    scenes = {
        'PORTADA': PORTRAIT('SEGUNDA'),
        'SEGUNDA': GAME1('SEGUNDA'),


    }
    scene = scenes['PORTADA']

    # Start running game loop
    run=True
    while run:
        # RGB - Red, Green, Blue
        screen.fill ((255,255,255))
        
        # Background img
        screen.blit(fondoImg, (0,0))

        # EVENTS 
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: # Si el evento es salir de la ventana, terminamos
                run = False

        # Scene managment??    
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