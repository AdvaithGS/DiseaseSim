import renderer as gui
import particles as prt
import pygame
from random import sample,choice

NumInfected = 1
NumParticles = 20
Move_Freq = 75
Speed = 2
InfRate = 0.8
DetRate = 0.8
FramesRecover = 700
Quarn = False

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
# Creates first pool object
quarantine = prt.pool(e = 1,name = "Quarantine")
quarantine.setdomain(((-450,200), (-200,0)),WHITE)

# Creates second pool object
pool1 = prt.pool(e = 1,name = "Pool 1")
pool1.setdomain(((-150, 375), (150, 50)),WHITE)

pool2 = prt.pool(e = 1,name = "Pool 2")
pool2.setdomain(((-150,0), (150, -325)),WHITE)

pool3 = prt.pool(e = 1,name = "Pool 3")
pool3.setdomain(((175,375), (475, 50)),WHITE)

pool4 = prt.pool(e = 1,name = "Pool 4")
pool4.setdomain(((175,0), (475, -325)),WHITE)

#Background
background = prt.pool(collisions= False,e = 1,name = "Background")
background.setdomain(((-500,400), (500, -400)),color = BLACK)

pool5 = prt.pool(e = 1,name = "Pool 5")
pool5.setdomain(((-475,-100), (-175, -325)),WHITE)


# Initializes particles randomly
pool1.random(NumParticles, Speed, 7)
pool2.random(NumParticles, Speed, 7)
pool3.random(NumParticles, Speed, 7)
pool4.random(NumParticles, Speed, 7)

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


pools = [pool1,pool2,pool3,pool4,pool5,quarantine,background]
particle_pools  = [pool1,pool2,pool3,pool4]

for i in sample(pool1.particles + pool2.particles,NumInfected):
	i.status = "Infected"
	i.infected = 0


started = False
i = 0

def Start():
	global started
	started = not started
	if(buttons[0].buttonText == "Start"):
		buttons[0].buttonText = "Pause"
	elif buttons[0].buttonText == "Pause":
		buttons[0].buttonText = "Resume"
	elif buttons[0].buttonText == "Resume":
		buttons[0].buttonText = "Pause"


buttons = [gui.Button(60, 100, 200, 50, 'Start', Start),gui.Button(60, 30, 200, 50, 'Quarantine', Quarantine,fillColors = {
        'normal': '#ff0000',
        'hover': '#660000',
        'pressed': '#330000',
    })]

played_frames = 0
d :list = [0,0,0] #S,I,R
moving = True
history = []
while True:
	i += 1
	pygame.time.Clock().tick(144)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.display.quit()
			pygame.quit()
			quit()


	for b in buttons:
			b.process(i)
	d = [0,0,0]

	for p in pools:
		if(i == 1):
			p.update(InfRate,FramesRecover,Quarn, DetRate,quarantine,background)
		gui.drawpool(p)
		for x in p.particles:
			d[{"Susceptible":0,"Infected":1,"Recovered":2}[x.status]] += 1
	
	gui.drawgraph(d,played_frames,NumParticles*4,history,new=(played_frames%10==0 and started and played_frames < 2985))	

	if(started):
		played_frames += 1
		if(moving and not(played_frames%Move_Freq)):
			while((x:=choice(choice(particle_pools).particles)).status == "Recovered"):
				pass
			x.move(choice([i for i in particle_pools if i != x.pool]),background)

		
		for p in pools:
			p.update(InfRate,FramesRecover,Quarn, DetRate,quarantine,background)
			gui.drawpool(p) 
		
		if(d[2]/(NumParticles*4) >= 0.75):
			moving = False
	
	gui.update() # Updates screenclear
