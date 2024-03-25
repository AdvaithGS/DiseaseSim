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
# Creates first pool object
quarantine = prt.pool(e = 1)
quarantine.setdomain(((-450,100), (-200,-100)))

background = prt.pool(e = 1)
background.setdomain(((-500,400), (-500,400)))

# Creates second pool object
pool1 = prt.pool(e = 1)
pool1.setdomain(((0,200), (450,-200)))

# Initializes particles randomly
pool1.random(NumParticles, Speed, 12)

def Quarantine():
	global Quarn
	Quarn = True

for i in sample(pool1.particles,NumInfected):
	i.status = "Infected"
	i.infected = 0

pools = [pool1,quarantine]

started = False

def Start():
	global started
	started = not started

i = 0 
buttons = [gui.Button(30, 200, 400, 100, 'Button One', Start),gui.Button(30, 30, 150, 100, 'Button One', Quarantine)]

while True:
	i += 1
	pygame.time.Clock().tick(144)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.display.quit()
			pygame.quit()
			quit()

	buttons[0].process(i)

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
