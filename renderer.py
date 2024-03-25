import pygame 
import time

pygame.init()

# inizializzazione pygame e finestra

WIDTH, HEIGHT = 1000, 1000
OFFW, OFFH = WIDTH//2, HEIGHT//2

WHITE = 255,255,255

schermo = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Particles')

font = pygame.font.SysFont('Arial', 40)

class Button():
	def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.onclickFunction = onclickFunction
		self.onePress = onePress
		self.alreadyPressed = False
		self.fillColors = {
        'normal': '#ffffff',
        'hover': '#666666',
        'pressed': '#333333',
    }
		self.buttonSurface = pygame.Surface((self.width, self.height))
		self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

	def process(self):
		mousePos = pygame.mouse.get_pos()
		self.buttonSurface.fill(self.fillColors['normal'])
		if self.buttonRect.collidepoint(mousePos):
			self.buttonSurface.fill(self.fillColors['hover'])
			if pygame.mouse.get_pressed(num_buttons=3)[0]:
				self.buttonSurface.fill(self.fillColors['pressed'])
				if self.onePress:
					self.onclickFunction()
				elif not self.alreadyPressed:
					self.onclickFunction()
					self.alreadyPressed = True
				else:
					self.alreadyPressed = False
					
		schermo.blit(self.buttonSurface, self.buttonRect)

schermo.fill(WHITE)


def update(background = (0,0,0)):
	pygame.display.update()
	schermo.fill(background)

def drawpool(pool):
	for p in pool.particles:
		pygame.draw.circle(schermo, p.color, (int(p.x) + OFFW, -int(p.y) + OFFH), int(p.r))

	for b in pool.obstacles:
		if type(b) == prt.barrier:
			if b.axys == 1:
				pygame.draw.line(schermo, b.color, (int(b.x0) + OFFW, -int(b.y) + OFFH), (int(b.x1) + OFFW, -int(b.y) + OFFH), 4)
			elif b.axys == 0:
				pygame.draw.line(schermo, b.color, (int(b.x) + OFFW, -int(b.y0) + OFFH), (int(b.x) + OFFW, -int(b.y1) + OFFH), 4)

	pygame.draw.rect(schermo, pool.cont.color, offsetrect(pool.cont, OFFW, OFFH), 2)

def offsetrect(rect, dx, dy):
	return (rect.x0 + dx, -rect.y0 + dy), (rect.x1 - rect.x0, -rect.y1 + rect.y0)
