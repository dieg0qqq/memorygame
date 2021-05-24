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

fade_event = pygame.USEREVENT + 1
fade_timer = 10

# PORTRAIT SCENE
class PORTRAIT:

    def __init__(self, next_scene):
        # Initialize variables
        self.background = pygame.Surface(size)

        self.flechaImg = pygame.image.load('flecha.png')
        self.flechaImg_rect = self.flechaImg.get_rect()
        self.flechaImg_rect = self.flechaImg_rect.move(1000,500)

        self.next_scene = next_scene
        
    def draw(self,screen, dt):
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
                    pygame.time.set_timer(fade_event, 1000)
                    return (self.next_scene, None)
                

class GAME1:
    def __init__(self, next_scene):
        self.background = pygame.Surface(size)
        
        self.fade = False
        self.fade_time = 0
        self.current_alpha = 255
        self.part = 1
                
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
       
    def draw(self,screen, dt):
        self.background = pygame.Surface(size)
        font = pygame.font.SysFont("comicsansms",50)

        self.correct_image_rect = self.rects[self.imagenes1_array.index('coche.png')]
        coche_img = pygame.image.load('coche.png').convert_alpha()
        # If we wanted to make it bigger:
        # coche_img = pygame.transform.scale(coche_img, (400,300))
        text1 = font.render('¡A recordar!',True, PURPLE)

        # First half     
        if self.part == 1 and not self.fade:
            # Show image to remember and then fade out
            screen.blit(text1, (500, 20))
            screen.blit(coche_img, (570, 300))
    
        elif self.part == 1 and self.fade:
            self.fade_time += dt
            if self.fade_time > fade_timer:
                self.fade_time = 0
                coche_img.set_alpha(self.current_alpha)
                text1.set_alpha(self.current_alpha)
               
                self.current_alpha -= 3
                if self.current_alpha == 0:
                   self.fade = False
                   self.part = 2
            # Blit the fade effect
            screen.blit(text1, (500, 20))
            screen.blit(coche_img, (570, 300)) 
    
        else:
            # Second half 
            text2 = font.render('¿Cuál era el dibujo?',True, PURPLE)
            screen.blit(text2, (450,10))

            # Show all similar images        
            for i in range(len(self.images)):
                screen.blit(self.images[i], (self.rects[i].x, self.rects[i].y))
    
    def update(self, events, dt):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.correct_image_rect.collidepoint(event.pos):
                        return ('CORRECT',CorrectScreen())
                for rect in self.rects:
                    if not self.correct_image_rect.collidepoint(event.pos) and rect.collidepoint(event.pos):
                        return ('INCORRECT',WrongScreen())


class CorrectScreen:
    def __init__(self):
        self.background = pygame.Surface(size)
        self.correct = pygame.image.load('correct.png')
        self.correct = pygame.transform.scale(self.correct, (400,400))

    def start(self, gamestate):
        self.gamestate = gamestate    

    def draw(self,screen,dt):
       self.background = pygame.Surface(size) 
       font = pygame.font.SysFont("comicsansms",50)
       text = font.render('¡Correcto!', True, GREEN)
       screen.blit(text, (500, 200))
       screen.blit(self.correct, (500,200))

    def update(self, events, dt):
       for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN: 
                print('ok')

class WrongScreen:                        
    def __init__(self):
        self.background = pygame.Surface(size)
        self.incorrect = pygame.image.load('incorrect.png')
        self.incorrect = pygame.transform.scale(self.incorrect, (400,400))

    def start(self, gamestate):
        self.gamestate = gamestate    

    def draw(self,screen,dt):
       self.background = pygame.Surface(size) 
       font = pygame.font.SysFont("comicsansms",50)
       text = font.render('¡Incorrecto!', True, RED)
       screen.blit(text, (500, 200))
       screen.blit(self.incorrect, (500,200))

    def update(self, events, dt):
       for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN: 
                print('ok')


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
        'CORRECT': CorrectScreen(),
        'INCORRECT': WrongScreen(),


    }
    scene = scenes['PORTADA']

    # Start running game loop
    run=True
    while run:
        
        # Background img
        screen.blit(fondoImg, (0,0))

        # EVENTS 
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: # Si el evento es salir de la ventana, terminamos
                run = False
            if event.type == fade_event:
                scene.fade = True
                pygame.time.set_timer(fade_event, 0)
                print("fade event")
     
        # Scene managment??    
        result = scene.update(events, dt)
        if result:
            next_scene, state = result
            if next_scene:
                scene = scenes[next_scene]
                scene.start(state)
       
        scene.draw(screen, dt)
        pygame.display.flip()
        dt = clock.tick(60)
        #pygame.display.update()
   

if __name__ == '__main__':
    main()