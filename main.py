import renderer as gui
import particles as prt
import pygame
from random import sample


NumInfected = 1
NumParticles = 30
Speed = 5
InfRate = 0.2
DetRate = 0.8
FramesRecover = 500
Quarn = False

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
# Creates first pool object
quarantine = prt.pool(e = 1)
quarantine.setdomain(((-450,100), (-200,-100)),WHITE)

# Creates second pool object
pool1 = prt.pool(e = 1)
pool1.setdomain(((-150, 375), (150, 50)),WHITE)

pool2 = prt.pool(e = 1)
pool2.setdomain(((-150,0), (150, -325)),WHITE)

pool3 = prt.pool(e = 1)
pool3.setdomain(((175,375), (475, 50)),WHITE)

pool4 = prt.pool(e = 1)
pool4.setdomain(((175,0), (475, -325)),WHITE)

#Background
background = prt.pool(e = 1)
background.setdomain(((-500,400), (500, -400)),color = BLACK)

# Initializes particles randomly
pool1.random(1, Speed, 7)
# pool2.random(NumParticles, Speed, 7)
# pool3.random(NumParticles, Speed, 7)
# pool4.random(NumParticles, Speed, 7)

def Quarantine():
	global Quarn
	Quarn = not Quarn
	if(buttons[1].fillColors['normal'] == "#ff0000"):
		buttons[1].fillColors = {
        'normal': '#00ff00',
        'hover': '#006600',
        'pressed': '#003300',
    }
	else:
		buttons[1].fillColors = {
        'normal': '#ff0000',
        'hover': '#660000',
        'pressed': '#330000',
    }


pools = [pool1,pool2,pool3,pool4,quarantine,background]

# for i in sample(pool1.particles + pool2.particles,NumInfected):
# 	i.status = "Infected"
# 	i.infected = 0


started = False
i = 0

def Start():
	global started
	started = not started
	if(buttons[0].buttonText == "Start"):
		buttons[0].buttonText = "Pause"
	elif buttons[0].buttonText == "Pause":
		buttons[0].buttonText = "Resume"


buttons = [gui.Button(60, 100, 200, 50, 'Start', Start),gui.Button(60, 30, 200, 50, 'Quarantine', Quarantine,fillColors = {
        'normal': '#ff0000',
        'hover': '#660000',
        'pressed': '#330000',
    })]
for pool in pools:
	print(((pool.cont.x0+pool.cont.x1)/2,(pool.cont.y0+pool.cont.y1)/2))

while True:
	i += 1
	pygame.time.Clock().tick(144)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.display.quit()
			pygame.quit()
			quit()

	if i == 1000:
		pool1.particles[0].move(pool2,background)

	for b in buttons:
			b.process(i)

	for x in pools:
		if(i == 1):
			x.update(InfRate,FramesRecover,Quarn, DetRate,quarantine)
		gui.drawpool(x)

	if(started):
		# Updates and renders all pools
		for b in buttons:
			b.process(i)

		for p in pools:
			p.update(InfRate,FramesRecover,Quarn, DetRate,quarantine)
			gui.drawpool(p) 

	gui.update() # Updates screenclear
