# Some comments:  I have changed a load of things.  The main game is now a class not just a def. There is a scene class which is the base class for the different scenes (intro, game, correct/incorrect scenes). 

# One of the issues which you have ran into is the scene management.  Usually you would do it similar to how you had it before, with the dictionary of scenes with their names and next scenes:

#   scenes = {
#        'PORTADA': PORTRAIT('SEGUNDA'),
#        'SEGUNDA': GAME1('SEGUNDA'),
#        'CORRECT': CorrectScreen(),
#        'INCORRECT': WrongScreen(),
#    }

# So if this was a standard game with an intro screen, the game, and a high scores screen it would look like this:

#     scenes = {
#        'PORTADA': Intro('SEGUNDA'),
#        'SEGUNDA': Game('Highs'),
#        'Highs': Highscore_screen("PORTADA")
#       }

# and it would start at the intro screen, go on to the game, then the high scores and then loop back to the intro

# The issue here is having the correct and incorrect screens and then looping back and having another scene, so we have to do it a different way. SO what we have is that each scene sends back the next scene.  The intro scene sends back "next_game", the game sends back either "correct" or "incorrect" and we show one of those, and they also send back "next_game" and the game plays again.

# We fade the correct and incorrect images out like in the game, and clicking the flecha image moves to the next game

# If you have any questions, please message me on reddit (not that useless chat thing - I only seem to get chat notifications several hours after someone has sent me something on there lol!)

# Import libraries
import os, sys, pygame, pygame.freetype, random
from pygame.locals import *

# Set size of window
size = 1280,768

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

# the fade events placed into the event queue by the timer 
fade_event = pygame.USEREVENT + 1
fade_timer = 10

# this sets the image directory. They are in the same place as the code at present, so we just use this:
img_dir1 = os.path.join(os.path.dirname(__file__), "Imgs1")
img_dir2 = os.path.join(os.path.dirname(__file__), "Imgs2")

# you could put the images in their own folder and use this to set the img_dir, as long as the image dir was called "img"!:
# img_dir = path.join(path.dirname(__file__), "img")

# we load the images here so they are accessible throughout
images1 = [] 
files = os.listdir(img_dir1)
for file in files:
	img = pygame.image.load(file)
	images1.append(img)

images2 = [] 
files = os.listdir(img_dir2)
for file in files:
	img = pygame.image.load(file)
	images2.append(img)

# we make a dictionary for the levels and images, so we can switch images using the level (1,2) as the dictionary key, i.e. we can just do:
# for img in level_dict[self.level]:
# so 1 is the key for the images1 list and 2 is the key for the images 2 list, so we can use the level as a key to get the images for that level.	
level_dict = { 1 : images1, 2 : images2 }

# the background image
background_img = pygame.image.load('fondo_memory.png')

# the arrows image
flechaImg = pygame.image.load('flecha.png')

# set a font for use throughout
font = pygame.font.SysFont("comicsansms", 70)

# utility function to draw text on the screen - this is unused, I thought it might be useful.  It would be easy to convert the game to use it.
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font("comicsansms", size)
    text_surface = font.render(text, True, PURPLE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)

    surface.blit(text_surface, text_rect)   

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

# this is the base class for the scenes.  All the scenes inherit from this class
# so have a get_events() and draw() method
# sometimes they will have their own draw method but that will call this draw 
# using the super() keyword. This means all scenes will have the same 
# background and the flecha image

class Scene(pygame.Surface):
    def __init__(self, game_images, name, next_scene):
        self.game_images = game_images
        self.name = name
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

    def __init__(self, images = None, name = "Intro", next_scene = "next_game"):
       super().__init__(images, name, next_scene)

       self.flechaImg_rect = flechaImg.get_rect()
       self.flechaImg_rect.move_ip(1000,500)

    def draw(self, surf):
        super().draw(surf)
        img = font.render('Memory',True, PURPLE)
        surf.blit(img, (500,334)) 
        surf.blit(flechaImg, self.flechaImg_rect)

class GameScene(Scene):
	def __init__(self, game, images, main_image, name, next_scene):
		super().__init__(images, name, next_scene)
		
		self.game = game
		self.main_image = main_image

		# Fade effect set-up
		self.fade = False
		self.fade_time = 0
		self.current_alpha = 255
		self.part = 1
		
		self.record_text = font.render('¡A recordar!',True, PURPLE)
		self.correct_image_rect = None

		# Trying to use colliderect so it doesnt overlap
		# this is the same code as before but adapted to use the gameimage class and the rects stored there

		self.rects = []

		for i in self.game_images:
			position_set = False 
			while not position_set:
				x = random.randint(200,840)
				y = random.randint(100,600) 

				i.rect.x = x
				i.rect.y = y

				margin = 10
				rl = [rect.inflate(margin*2, margin*2) for rect in self.rects]
				if len(self.rects) == 0 or i.rect.collidelist(rl) < 0:
					self.rects.append(i.rect)
					position_set = True

		# this makes a number and object pair, and allows us to set the correct rects for the correct gameimage classes
		for i, rect in enumerate(self.rects):
			self.game_images[i].rect = rect

	# this is the fade stuff from before that was in draw. It really belongs here tbh
	def update(self, dt):
		if self.part == 1 and self.fade:
			self.fade_time += dt
			if self.fade_time > fade_timer:
				self.fade_time = 0
				self.main_image.set_alpha(self.current_alpha)
				self.record_text.set_alpha(self.current_alpha)

				self.current_alpha -= 3
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
			screen.blit(self.record_text, (450, 20))
			screen.blit(self.main_image.image, (570, 300)) 

		else:
			# Second half 
			text2 = font.render('¿Cuál era el dibujo?',True, PURPLE)
			screen.blit(text2, (350,10))

			# Show all similar images	   
			for game_image in self.game_images:
				game_image.draw(screen)

			# We associate the correct rect to the correct image, to pass it later to the CORRECT Screen
			self.correct_image_rect = self.game_images[self.game_images.index(self.main_image)].rect

	# again we pass the event to the game object the same as with the other classes
	def get_event(self, event):
		if self.part == 2:
			if self.correct_image_rect.collidepoint(event.pos):
				self.game.score += 1
				return 'CORRECT'
			for rect in self.rects:
				if not self.correct_image_rect.collidepoint(event.pos) and rect.collidepoint(event.pos):
					return 'INCORRECT'    

# These are the correct and incorrect scenes that come up when the player clicks on one of the images
class CorrectScene(Scene):
    def __init__(self):
        super().__init__(None, "correct", "next_game")
        self.correct = pygame.image.load('correct.png')
        self.correct = pygame.transform.scale(self.correct, (400,400))
        self.flechaImg_rect = flechaImg.get_rect()
        self.flechaImg_rect.move_ip(1000,500)

    def draw(self, surf):
        super().draw(surf)
        text = font.render('¡Correcto!', True, GREEN)
        surf.blit(text, (500, 40))
        surf.blit(self.correct, (500,180))
        surf.blit(flechaImg, self.flechaImg_rect)

class IncorrectScene(Scene):                        
    def __init__(self):
        super().__init__(None, "incorrect", "next_game")
        self.incorrect = pygame.image.load('incorrect.png')
        self.incorrect = pygame.transform.scale(self.incorrect, (400,400))
        self.flechaImg_rect = flechaImg.get_rect()
        self.flechaImg_rect.move_ip(1000,500)

    def draw(self, surf):
        super().draw(surf)
        font = pygame.font.SysFont("comicsansms",50)
        text = font.render('¡Incorrecto!', True, RED)
        surf.blit(text, (500, 40))
        surf.blit(self.incorrect, (450,180))
        surf.blit(flechaImg, self.flechaImg_rect)
# this shows the score and asks if the player wants to play again
class ScoreScene(Scene):
	def __init__(self, score):
		super().__init__(None, "Score", "new_game")
		self.score = str(score)
		self.score_surf = font.render(self.score, True, RED)
		self.play_again = font.render("Play again?", True, RED)

		self.yes = font.render("Yes!", True, RED, BLUE)
		self.yes_rect = self.yes.get_rect()
		self.yes_rect.move_ip(500, 380)

		self.no = font.render("No", True, RED, BLUE)
		self.no_rect = self.no.get_rect()
		self.no_rect.move_ip(650, 380)
	
	def get_event(self, event):
		mouse_pos = event.pos
		if self.no_rect.collidepoint(mouse_pos):
			pygame.quit()
			sys.exit()
		elif self.yes_rect.collidepoint(mouse_pos):
			return self.next_scene

	def draw(self, surf):
		super().draw(surf)
		font = pygame.font.SysFont("comicsansms",50)
		text = font.render('Score', True, RED)
		surf.blit(text, (500, 40))
		surf.blit(self.score_surf, (450,180))
		surf.blit(self.play_again, (450, 280))
		surf.blit(self.yes, self.yes_rect)
		surf.blit(self.no, self.no_rect)

# instead of just doing def main(), we create a class to run everything
class MemoryGame(object):
    def __init__(self):
        # all the initalisation is done here
        # Definimos las dimensiones de la ventana (1600 x 900px) y reloj
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()

        # Ponemos el título e icono y fondo de la ventana
        pygame.display.set_caption("Memory")
        icon = pygame.image.load('icon.png')
        pygame.display.set_icon(icon)

        # Para los niveles y puntuación
        self.level = 1
        self.max_level = 2
        self.game_counter = 0
		
        self.score = 0
        # Creamos un nuevo nivel
        self.new_level()

        # we set the self.scene to point to an instance of the IntroScene
        # and self.next_scene is set to None
        self.Intro = IntroScene()
        self.scene = self.Intro
        self.next_scene = None

    def new_level(self):
        self.game_images = []

		# we create some GameImage objects here with the images passed to them
		# they will create their rects and we will let the gamescene class
		# reposition them
		
        for img in level_dict[self.level]:
	        game_image = GameImage(img)
	        self.game_images.append(game_image)

    # this is called when we restart the game. It just sets score to 0, level to 1 and so on
    def new_game(self):
        self.score = 0
        self.level = 1
        self.game_counter = 0
        self.new_level()
        self.next_scene = "next_game"
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
                self.next_scene = self.scene.get_event(event)

    # the update function. If next scene is None we are in the middle of the game and just update the game
    # else if one of the classes sets next_scene we move to the next_scene. 
    def update(self, dt):
        if self.next_scene is None:
            self.scene.update(dt)
            return

        elif self.next_scene == "CORRECT":
            self.score += 1
            self.scene = CorrectScene()
        elif self.next_scene == "INCORRECT":
            self.scene = IncorrectScene()
        elif self.next_scene == "next_game":
            main_image = random.choice(self.game_images)
            self.scene = GameScene(self, self.game_images, main_image, "game", "Score") 
            self.game_counter += 1
            
            if self.game_counter == 2:
                self.game_counter = 0
                if self.level < self.max_level:
                    self.level += 1
                    self.new_level()	
                else:
                    self.next_scene = "Score"
                    self.update(0)
        elif self.next_scene == "Score":
            self.scene = ScoreScene(self.score)
        elif self.next_scene == "new_game":
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