import math
from random import randint, uniform, random
from numpy import sign

class particle:
	def __init__(self, pos, vel, r,pool):
		self.x = pos[0]
		self.y = pos[1]
		self.xv = vel[0]
		self.yv = vel[1]
		self.status = "Susceptible"
		self.infected = 0
		self.pool = pool
		self.r = r
		self.color = (0,0,255)
		self.container = None

	def update(self,frames,quarn):
		self.x += self.xv
		self.y += self.yv
		self.speed = math.sqrt(self.xv**2 + self.yv**2)
		self.infected += 1
		if(self.status == "Infected" and self.infected > frames):
			self.status = "Recovered"
			self.infected = 0

		self.color = getcolor(self.status)

	def collide(self, body, E,rate,quarn,detection,quarantine):
		dx, dy = self.x - body.x, self.y - body.y #vector difference in position
		d = math.sqrt(dx**2 + dy**2)
		
		# Has collided
		if d < self.r + body.r:
			dvx, dvy = self.xv - body.xv, self.yv - body.yv #vector difference in speeds
			sin, cos = dx/d, dy/d 
			dr = (self.r + body.r - d) / 2
			dx2, dy2 = sin * dr, cos * dr

			self.x += dx2
			self.y += dy2
			body.x -= dx2
			body.y -= dy2

			h = (dx * dvx + dy * dvy) / d
			new_dvx, new_dvy = -h * sin * E, -h * cos * E

			self.xv += new_dvx
			self.yv += new_dvy
			body.xv -= new_dvx
			body.yv -= new_dvy

			if(((self.status,body.status) in [("Infected","Susceptible"),("Susceptible","Infected")]) and random() <= rate):
				if(body.status == 'Infected'):
					self.status = "Infected"
					self.infected = 0
					if(quarn and random() <= detection):
						x = self.pool
						x.removepcl(self)
						self.pool = quarantine
						quarantine.particles.append(self)
				else:
					body.status = "Infected"
					body.infected = 0
					if(quarn and random() <= detection):
						x = body.pool
						x.removepcl(body)
						body.pool = quarantine
						quarantine.particles.append(body)


def clamp(n, min, max):
	if min < n < max:
		return n
	elif n >= max:
		return max
	else:
		return min

def getcolor(status):
	if status == "Infected":
		return (255,0,0)
	elif status == "Susceptible":
		return (0,0,255)
	elif status == "Recovered":
		return (128,128,128)
	else:
		print(status)
		return (0,0,255)

class obstacle:
	color = (255,255,255)
	e = 1
	tag = None
	def collide(self, p, E):
		pass

class barrier(obstacle):
	def __init__(self, axys, x, y, l, tag = None):
		self.tag = tag
		if axys == 1 or axys == 'x':
			self.axys = 1
			self.y = y
			self.x0 = x - l/2
			self.x1 = x + l/2
		elif axys == 0 or axys == 'y':
			self.axys = 0
			self.x = x
			self.y0 = y - l/2
			self.y1 = y + l/2
		else:
			print("invalid axys")

	def collide(self, p, E):
		if self.axys == 1:
			intersect = abs(p.y - self.y) - p.r
			if self.x0 < p.x < self.x1 and intersect < 0:
				p.y += intersect * sign(p.yv)
				p.yv = - p.yv * E * self.e
		else:
			intersect = abs(p.x - self.x) - p.r
			if self.y0 < p.y < self.y1 and intersect < 0:
				p.x += intersect * sign(p.xv)
				p.xv = - p.xv * E * self.e

class _container(obstacle):
	def __init__(self, rect):
		self.rect = rect
		self.x0 = rect[0][0]
		self.y0 = rect[0][1]
		self.x1 = rect[1][0]
		self.y1 = rect[1][1]

	def collide(self, p, E):
		if p.y + p.r > self.y0:
			p.y -= p.r + p.y - self.y0
			p.yv = -p.yv * E
		elif p.y - p.r < self.y1:
			p.y += p.r - p.y + self.y1
			p.yv = -p.yv * E
		if p.x + p.r > self.x1:
			p.x -= p.r + p.x - self.x1
			p.xv = -p.xv * E
		elif p.x - p.r < self.x0:
			p.x += p.r - p.x + self.x0
			p.xv = -p.xv * E

class pool:

	def __init__(self, e = 1, *particles):
		self.particles = []
		self.obstacles = []
		self.cont = _container(((-10000,10000), (10000,-10000)))
		self.e = e
		for p in particles:
			self.add(p)

	def add(self, body):
		if issubclass(type(body), obstacle):
			self.obstacles.append(body)
		elif type(body) == particle:
			self.particles.append(body)

	def merge(self, pool2):
		self.particles += pool2.particles
		self.obstacles += pool2.obstacles

	def update(self,rate,frames,quarn,detection,quarantine):
		e = self.e *.5 + .5
		for p in self.particles:
			p.update(frames,quarn)
		for i, p in enumerate(self.particles):
			for p2 in self.particles[i+1:]:
				p.collide(p2, e,rate,quarn,detection,quarantine)

			for b in self.obstacles:
				b.collide(p, e)
			self.cont.collide(p, e)

	def setdomain(self, rect):
		self.cont = _container(rect)

	def removeob(self, tag):
		self.obstacles = [item for item in self.obstacles if item.tag != tag]

	def removepcl(self, particle : particle):
		self.particles.remove(particle)

	def random(self, n, v, r, rect = None):
		if rect is None:
			rect = self.cont.rect
			print(rect)
		for _ in range(n):
			p = particle((randint(rect[0][0], rect[1][0]), randint(rect[1][1], rect[0][1])), (uniform(-v, v), uniform(-v, v)), r,self)
			self.add(p)


def mergepools(*pools, e = False):
	if not e:
		e = pools[0].e
	newpool = pool(e = e)
	for p in pools:
		newpool.particles += p.particles
		newpool.obstacles += p.obstacles
	return newpool

