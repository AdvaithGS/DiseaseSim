import pygame 
import particles

pygame.init()

# inizializzazione pygame e finestra

WIDTH, HEIGHT = 1000, 800
OFFW, OFFH = WIDTH//2, HEIGHT//2

WHITE = 255,255,255

schermo = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Particles')

font = pygame.font.SysFont('Roboto', 40)

class Button():
	def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False, fillColors : dict  = {
        'normal': '#ffffff',
        'hover': '#666666',
        'pressed': '#333333',
    }):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.onclickFunction = onclickFunction
		self.onePress = onePress
		self.alreadyPressed = False
		self.LastPressed = 0
		self.fillColors = fillColors
		self.buttonText = buttonText
		self.buttonSurface = pygame.Surface((self.width, self.height))
		self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.buttonSurf = font.render(self.buttonText, True, (20, 20, 20))
		# self.buttonRect = self.buttonSurf.get_rect(center = (self.x,self.y))

	def process(self,n):
		mousePos = pygame.mouse.get_pos()
		self.buttonSurface.fill(self.fillColors['normal'])
		if self.buttonRect.collidepoint(mousePos):
			self.buttonSurface.fill(self.fillColors['hover'])
			if pygame.mouse.get_pressed(num_buttons=3)[0]:
				self.buttonSurface.fill(self.fillColors['pressed'])
				if self.onePress and (n-self.LastPressed) >= 30:
					self.onclickFunction()
					self.LastPressed = n
				elif not self.alreadyPressed and (n-self.LastPressed) >= 30:
					self.onclickFunction()
					self.alreadyPressed = True
					self.LastPressed = n
				else:
					self.alreadyPressed = False
		self.buttonSurf = font.render(self.buttonText, True, (20, 20, 20))
		schermo.blit(self.buttonSurface, self.buttonRect)
		schermo.blit(self.buttonSurf, self.buttonRect)

schermo.fill(WHITE)


def update(background = (0,0,0)):
	pygame.display.update()
	schermo.fill(background)

def drawpool(pool):
	for p in pool.particles:
		pygame.draw.circle(schermo, p.color, (int(p.x) + OFFW, -int(p.y) + OFFH), int(p.r))
	# pygame.draw.circle(schermo,(0,255,0),(pool.cont.x0,pool.cont.y0),5)

	for b in pool.obstacles:
		if type(b) == particles.barrier:
			if b.axys == 1:
				pygame.draw.line(schermo, b.color, (int(b.x0) + OFFW, -int(b.y) + OFFH), (int(b.x1) + OFFW, -int(b.y) + OFFH), 4)
			elif b.axys == 0:
				pygame.draw.line(schermo, b.color, (int(b.x) + OFFW, -int(b.y0) + OFFH), (int(b.x) + OFFW, -int(b.y1) + OFFH), 4)

	pygame.draw.rect(schermo, pool.cont.color, offsetrect(pool.cont, OFFW, OFFH), 2)

def offsetrect(rect, dx, dy):
	return (rect.x0 + dx, -rect.y0 + dy), (rect.x1 - rect.x0, -rect.y1 + rect.y0)
