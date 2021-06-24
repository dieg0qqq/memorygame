# Import libraries
import os, sys, pygame, pygame.freetype, pygame.mixer, random
from pygame.locals import *

# Set size of window
size = 1280,768
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 768

# Colours   R   G   B
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

# init pygame
pygame.init()
pygame.mixer.init()

# inititialise the screen here
screen = pygame.display.set_mode(size)
screenrect = screen.get_rect()

# the fade events placed into the event queue by the timer 
fade_event = pygame.USEREVENT + 1
fade_timer = 10

# this is a utility class to store an image and its rect in one place:
class GameImage(object):
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()

    # this class has the set_alpha so the alpha can be passed on to its image
    def set_alpha(self, alpha):
        self.image.set_alpha(alpha)

    # we pass the draw method the surface we want the image drawn on
    def draw(self, surf):
        surf.blit(self.image, self.rect)

# we make a dictionary for the game_image objects and create them here when we load the images.  The level is the index into this in 
# the game, so we can switch between them using that. Hence, 1 is the key for the level 1 game_image objects and so on
game_images_dict = {}

# we load the images here so they are accessible throughout. we use os.listdir which just returns a list of strings which are the filenames of
# the files in that directory. Then we iterate throught them, load the image using pygame.image.load, and create the game_image object
# from the loaded images and add them to a list, and set that as the value for the key. Index is the key for the dictionary.
index  = 0

for filename in os.listdir():
    if filename.startswith("Imgs"):
        images = []
        
        files = os.listdir(filename)
        for file in files:
            img = pygame.image.load(os.path.join(filename, file))
            img.set_colorkey(WHITE)
            images.append(GameImage(img))

        game_images_dict[index] = images
        index += 1

# subtract one from index so it is now the same as the amount of levels


# the background image
background_img = pygame.image.load('fondo_memory.png')

# the arrows image
flechaImg = pygame.image.load('flecha.png')

# here we load the correct and incorrect images which are displayed to the user
correct_img = pygame.image.load('correct.png')
correct_img = pygame.transform.scale(correct_img, (400,400))

incorrect_img = pygame.image.load('incorrect.png')
incorrect_img = pygame.transform.scale(incorrect_img, (400,400))

# set a font for use throughout
font = pygame.font.SysFont("comicsansms", 70)

# level names

level_names = ["Colores I", "Colores II", "Formas Geométricas 2D", "Formas Geométricas 3D", 
"Dibujos Animales", "Dibujos Transportes", "Letras", 
"Palabras Mayúsculas","Palabras Minúsculas" ,"Pictogramas Emociones I", 
"Pictogramas Emociones II", "Fotos Emociones", "Personas en Acción",]

# simple button class for the menu
class Button(pygame.Surface):
    def __init__(self, text):
        
        self.text = text
        font = pygame.font.SysFont("comicsansms", 30)
        self.text_surf = font.render(text, True, PURPLE)
        self.text_surf2 = font.render(text, True, RED)
        width = self.text_surf.get_width()
        height = self.text_surf.get_height()
        
        super().__init__((width, height), flags=SRCALPHA)
        self.rect = self.get_rect()
           
        self.selected_surf = pygame.Surface((self.rect.width, self.rect.height))
        self.selected_surf.fill(WHITE)
        self.selected = False
        self.blit(self.text_surf, (0,0))
   
    def update(self):
        if self.selected:
            self.blit(self.selected_surf, (0, 0)) #, special_flags=pygame.BLEND_MULT)
            self.blit(self.text_surf2, (0,0))
        else:
            self.blit(self.text_surf, (0,0))
           
    def draw(self, surf):
        surf.blit(self, self.rect)
    
    def __str__(self):
    	data = "text = " + self.text + "\n"
    	data += "rect = " + str(self.rect)
    	
    	return data 
    
# this is the base class for the scenes.  All the scenes inherit from this class
# so have a get_events() and draw() method
# sometimes they will have their own draw method but that will call this draw 
# using the super() keyword. This means all scenes will have the same 
# background and the flecha image

class Scene(pygame.Surface):
    def __init__(self, next_scene):
        self.rect = pygame.Rect(screenrect)
        self.next_scene = next_scene

        # it has the background image and the flecha img
        # so all scenes can use the same background and the flecha img
        self.background_img = background_img 
        self.flechaImg_rect = flechaImg.get_rect()
        self.flechaImg_rect.move_ip(1000,500)  

    def get_event(self, event):
        mouse_pos = event.pos
        if self.flechaImg_rect.collidepoint(mouse_pos):
            pygame.time.set_timer(fade_event, 1000)
            return self.next_scene

    # there is an update here that does nothing update is called in the main loop and the IntroScene has no updating to do
    # so it would crash otherwise when we tried to call update on the IntroScene (hope that makes sense!)
    def update(self, dt):
        pass

    def draw(self, surf):
        surf.blit(self.background_img, (0,0))
        
class IntroScene(Scene):

    def __init__(self, next_scene):
       super().__init__(next_scene)

       self.flechaImg_rect = flechaImg.get_rect()
       self.flechaImg_rect.move_ip(1000,500)

    def draw(self, surf):
        super().draw(surf)
        img = font.render('Memory',True, PURPLE)
        img_rect = img.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        surf.blit(img, img_rect) 
        surf.blit(flechaImg, self.flechaImg_rect)

class MenuScene(Scene):

    def __init__(self, game):
        super().__init__(None)
        self.game = game
        self.flechaImg_rect = flechaImg.get_rect()
        self.flechaImg_rect.move_ip(1000,500)

        y = 100
        self.level_buttons = []

        for count in range(index):
            level_text = level_names[count]
            b = Button(level_text)
            b.rect.centerx = screenrect.centerx
            b.rect.y = y
            y += 50
            self.level_buttons.append(b)

    def get_event(self, event):
        for i, button in enumerate(self.level_buttons):
            if button.rect.collidepoint(event.pos):
                 if event.type == pygame.MOUSEBUTTONDOWN:
                     self.game.set_level(i)
                     return "next_game"
                 else:
                      button.selected = True
                      button.update()
            
            elif self.flechaImg_rect.collidepoint(event.pos):
                pygame.time.set_timer(fade_event, 1000)
                return "next_game"

            else:
                button.selected = False
                button.update()

    def draw(self, surf):
        super().draw(surf)
        font_name = pygame.font.SysFont("comicsansms", 60)
        img = font_name.render('Niveles',True, BLACK)
        img_rect = img.get_rect(center=(SCREEN_WIDTH/2, 50))
        surf.blit(img, img_rect) 

        for button in self.level_buttons:
            button.draw(surf)

        surf.blit(flechaImg, self.flechaImg_rect)
            
class GameScene(Scene):
    def __init__(self, game, images, main_image, next_scene):
        super().__init__(next_scene)
        
        self.game = game
        self.main_image = main_image
        self.game_images = images

        # Fade effect set-up
        self.fade = False
        self.fade_time = 0
        self.current_alpha = 255
        self.part = 1

        self.record_text = font.render('Atiende',True, PURPLE)
        self.record_text_rect = self.record_text.get_rect(center=(SCREEN_WIDTH/2, 70))
        self.correct_image_rect = None

        # Trying to use colliderect so it doesnt overlap
        # this is the same code as before but adapted to use the gameimage class and the rects stored there
        self.rects = []

    # this is the fade stuff from before that was in draw. It really belongs here tbh
    def update(self, dt):

        if len(self.rects) < len(self.game_images):
            i = len(self.rects)
            
            x = random.randint(100,950)
            y = random.randint(100,600) 

            self.game_images[i].rect.x = x
            self.game_images[i].rect.y = y

            margin = 5
            rl = [rect.inflate(margin*2, margin*2) for rect in self.rects]
            if len(self.rects) == 0 or self.game_images[i].rect.collidelist(rl) < 0:
                self.rects.append(self.game_images[i].rect)

        if self.part == 1 and self.fade:
            self.fade_time += dt
            if self.fade_time > fade_timer:
                self.fade_time = 0
                self.main_image.set_alpha(self.current_alpha)
                self.record_text.set_alpha(self.current_alpha)

                # Speed whichin the image dissapears
                self.current_alpha -= 5
                if self.current_alpha <= 0:
                    self.fade = False
                    self.part = 2

        else:
            # we reset the main image alpha otherwise it will be invisible on the next screen (yeah, this one caught me out lol!)
            self.main_image.set_alpha(255)

    # draw is similar to before, but a bit more streamlined as the fade stuff is not in update
    def draw(self, screen):
        super().draw(screen)

        if self.part == 1:
            screen.blit(self.record_text, self.record_text_rect)
            # x = self.main_image.rect.x.center
            # y = self.main_image.rect.y.center
            screen.blit(self.main_image.image, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)) 
        else:
            # Second half 
            text2 = font.render('¿Qué has visto?',True, PURPLE)
            screen.blit(text2, (400,5))

            # Show all similar images       
            cont = 0
            for game_image in self.game_images:
                game_image.draw(screen)
                cont += 1
            # We associate the correct rect to the correct image, to pass it later to the CORRECT Screen
            self.correct_image_rect = self.game_images[self.game_images.index(self.main_image)].rect

    # again we pass the event to the game object the same as with the other classes
    def get_event(self, event):
        if self.part == 2:
            if self.game.level == 13:
                self.game.game_over = True
            if self.correct_image_rect.collidepoint(event.pos):
                return 'CORRECT'
            for rect in self.rects:
                if not self.correct_image_rect.collidepoint(event.pos) and rect.collidepoint(event.pos):
                    return 'INCORRECT'    

class AnswerScene(Scene):
    def __init__(self, game, which_answer):
        self.game = game
        if not game.game_over:
            super().__init__("next_game")
        else:
            super().__init__("score")

        self.which_asnwer = which_answer
        self.flechaImg_rect = flechaImg.get_rect()
        self.flechaImg_rect.move_ip(1000,500)

        if self.which_asnwer == "correct":
            correct = pygame.mixer.Sound('correct.wav')
            correct.set_volume(1)
            pygame.mixer.find_channel().play(correct)
            self.image = correct_img.copy()
            self.text = font.render('¡Correcto!', True, GREEN)
        else:
            wrong = pygame.mixer.Sound('incorrect.wav')
            wrong.set_volume(1)
            pygame.mixer.find_channel().play(wrong)
            self.image = incorrect_img.copy()
            self.text = font.render('¡Incorrecto!', True, RED)

    def draw(self,surf):
        super().draw(surf)
        surf.blit(self.text, (500, 40))
        surf.blit(self.image, (490, 180))
        surf.blit(flechaImg, self.flechaImg_rect)

# this shows the score and asks if the player wants to play again
class ScoreScene(Scene):
    def __init__(self, score):
        super().__init__("new_game")
        self.score = str(score)
        self.score_surf = font.render(self.score, True, RED)
        self.score_surf_rect = self.score_surf.get_rect(center=(SCREEN_WIDTH/2, 330))
        self.play_again = font.render("¿Volver a jugar?", True, PURPLE)
        self.play_again_rect = self.play_again.get_rect(center=(SCREEN_WIDTH/2, 70))

        self.yes = font.render("¡Sí!", True, GREEN, NAVYBLUE)
        self.yes_rect = self.yes.get_rect()
        self.yes_rect.move_ip(500, 450)

        self.no = font.render("No", True, RED, NAVYBLUE)
        self.no_rect = self.no.get_rect()
        self.no_rect.move_ip(650, 450)
    
    def get_event(self, event):
        mouse_pos = event.pos
        if self.no_rect.collidepoint(mouse_pos):
            pygame.quit()
            sys.exit()
        elif self.yes_rect.collidepoint(mouse_pos):
            return self.next_scene

    def draw(self, surf):
        super().draw(surf)
        font = pygame.font.SysFont("comicsansms",60)
        text = font.render('Puntuación', True, PURPLE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, 200))
        surf.blit(text, text_rect)
        surf.blit(self.score_surf, self.score_surf_rect)
        surf.blit(self.play_again, self.play_again_rect)
        surf.blit(self.yes, self.yes_rect)
        surf.blit(self.no, self.no_rect)

# instead of just doing def main(), we create a class to run everything
class MemoryGame(object):
    def __init__(self):
        # all the initalisation is done here
        # Definimos las dimensiones de la ventana (1600 x 900px) y reloj
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        pygame.mixer.music.load('bckg_music.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        # Ponemos el título e icono y fondo de la ventana
        pygame.display.set_caption("Memory")
        icon = pygame.image.load('icon.png')
        pygame.display.set_icon(icon)

        # again we use a dict to store the game_image lists and use the level as the key
        self.game_images_dict = {}

        # Para los niveles y puntuación
        self.level = 0
        self.max_level = 13
        self.turn_counter = 0
        self.previous_image = None
        self.game_over = False
        self.score = 0

        # Creamos un nuevo nivel
        self.new_level()

        # we set the self.scene to point to an instance of the IntroScene and self.next_scene is set to None
        self.Intro = IntroScene("Menu")
        self.scene = self.Intro
        self.next_scene = None

    def new_level(self):
        self.turn_counter = 0
        self.game_images = game_images_dict[self.level]
        print(self.level)

    def set_level(self, level):
        self.turn_counter = 0
        self.game_images = game_images_dict[level]
        self.level = level
        pygame.time.set_timer(fade_event, 1000)
        
    # this is called when we restart the game. It just sets score to 0, level to 1 and so on
    def new_game(self):
        self.game_over = False
        self.score = 0
        self.level = 0
        
        self.new_level()
        self.next_scene = "Menu"
        pygame.time.set_timer(fade_event, 1000)
        self.update(0)
    
    # this is the main loop - the code just goes around this over and over
    def run(self):  
        # we use "running" as the name of our boolean to keep the 
        # loop running, as we don't want the name to clash with the method 
        # name, which is "run" and we also make it an object variable with
        # self so it can be referenced in the events method
        self.running = True
        while self.running:
            self.next_scene = None
            dt = self.clock.tick(30)
            self.events()
            self.update(dt)
            self.draw()

    # get the events and, if relevant, pass them to the scene classes
    def events(self):
        self.next_scene = None
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: # Si el evento es salir de la ventana, terminamos
                self.running = False

            elif event.type == fade_event:
                self.scene.fade = True
                pygame.time.set_timer(fade_event, 0)

            # the only event we are interested in in the scenes is the mousebuttondown event, so that is the 
            # only event we send. This is why the scenes don't check for event.type == pygame.MOUSEBUTTONDOWN.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mixer.Sound('click.wav')
                click.set_volume(0.3)
                pygame.mixer.find_channel().play(click)
                self.next_scene = self.scene.get_event(event)

            elif event.type == pygame.MOUSEMOTION:
                if isinstance(self.scene, MenuScene):
                    self.scene.get_event(event)
                    
    # the update function. If next scene is None we are in the middle of the game and just update the game
    # else if one of the classes sets next_scene we move to the next_scene. 
    def update(self, dt):
        if self.next_scene is None:
            self.scene.update(dt)
            return

        if self.next_scene == "CORRECT":
            self.score += 1
            self.scene = AnswerScene(self, "correct")
        elif self.next_scene == "INCORRECT":
            self.scene = AnswerScene(self, "incorrect")
        elif self.next_scene == "Menu":
            self.scene = MenuScene(self)
        elif self.next_scene == "next_game":
            main_image = self.previous_image
            self.turn_counter += 1

            while main_image == self.previous_image:
                main_image = random.choice(self.game_images)

            self.previous_image = main_image
            self.scene = GameScene(self,self.game_images,main_image, "Score")
            if self.turn_counter == 2:
                self.level += 1
                if self.level < self.max_level:
                    self.new_level()
        
        elif self.next_scene == "score":
            self.scene = ScoreScene(self.score)
            pygame.mixer.music.load('final3.wav')
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play()
        elif self.next_scene == "new_game":
            #pygame.mixer.music.load('bckg_music.mp3')
            #pygame.mixer.music.set_volume(0.2)
            #pygame.mixer.music.play(-1)
            self.new_game()

    # draw just passes the screen to the current scene so it can draw itself on it
    def draw(self): 
        self.scene.draw(self.screen)
        pygame.display.flip()

if __name__ == '__main__':
    m = MemoryGame()
    m.run()
    pygame.quit()
    quit()