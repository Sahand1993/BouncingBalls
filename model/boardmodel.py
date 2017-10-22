import numpy as np
import itertools
from numpy import subtract
from numpy.linalg import norm
from math import isclose, sqrt
import time

from model.exceptions.exceptions import ProximityError, OverlapError, ZeroError, ParentError, ArgumentError, WallOrientationError, TimeError

ERROR_TOL = 1

class Board:

	def __init__(self, width = 100, height = 100, sps = 2, slow = False):
		"""A board with (x,y) = (0,0) in the bottom left corner, 
		like the first quadrant of a coordinate system.

		width, height; no of cells
		sps; steps per second
		slow; True will put a sleep inside of the step()-loop.
		"""
		self.width = width
		self.height = height
		self.sps = 2
		self.timestep = 1/sps
		self.balls = set()
		self.ball_list = [] # Because I wanted to get the balls by order of addition when I was chasing a bug
		self.steps = 0 # This is the number of full timesteps taken.
		self.time_elapsed = 0
		self.walls = {}
		wall_positions = {
			1:self.height,
			2:self.width,
			3:0,
			4:0,
		}
		for i in range(4):
			self.walls[i+1] = Wall(self, i+1)

		self.slow = slow

	def add_ball(self, vx, vy, r, x = None, y= None, m = 1):
		"""
		x; position
		y; position
		radius; 
		vx; velocity on x-axis in cells per second. Has to be a whole number of cells. If you don't like it, up the resolution.
		vy; see vx
		"""
		if not x:
			x = self.width/2
		if not y:
			y = self.height/2

		if not self.overlap_new_ball(r, x, y):
			if self.ball_within_walls(r, x, y):
				ball = Ball(xpos = x, ypos = y, radius = r, vx = vx, vy = vy, mass = m, parent = self)
				self.balls.add(ball)
				self.ball_list.append(ball)
				return ball
			else:
				raise OverlapError("New ball is not within the confines of the board.")
		else:
			raise OverlapError("New ball overlaps with existing ball.")

	def get_ball_list(self):
		return list(self.balls)

	def get_balls_pygame(self):
		"""Returns a list of all ball radiuses, and positions in computer graphics coordinates."""
		return list(map(lambda ball: {
			'r':round(ball.r),
			'x': round(ball.x),
			'y': round(self.height-ball.y), ## Because the origin is in the upper left corner.
			}, self.balls))

	def step(self):
		"""This is to be executed before each step"""
		
		t_total = 0 #Total time progressed during the execution of this function
		ctr = 0
		while t_total < self.timestep: ######## SEEMS LIKE ENDLESS LOOP
			ctr += 1
			substep = self.timestep - t_total # Time that's left of timestep in current timestep
			contacts = self.first_contacts(substep) # get the balls that are touching in the first collision. contacts = {'time':time, 'collidors':[(ball_1,wall),(ball_1,ball_2),...]}
			if self.slow:
				time.sleep(1)


			if not contacts: # If we have no collisions during substep
				self.progress_balls(substep)
				break

			delta_t = contacts['time']

			if t_total + delta_t >= self.timestep: ## When we've gone over our timestep, we must progress all balls to the end of timestep, because no more collisions will take place inside of timestep.
				self.progress_balls(substep)
				break
			else:
				self.progress_balls(delta_t)
				t_total += delta_t

				for pair in contacts['collidors']:
					object1 = pair[0]
					object2 = pair[1]
					object1.collide(object2)



	def first_contacts(self, timestep):
		"""Returns a list of the balls that will touch at the time of the first collision."""

		ball_ball_contacts = self.first_ball_contacts(timestep) # ballpairs that are touching
		wall_ball_contacts = self.first_wall_contacts(timestep) # wall-ball pairs that are touching

		first_contacts = {}

		if ball_ball_contacts and wall_ball_contacts:

			if ball_ball_contacts['time'] == wall_ball_contacts['time']:
				first_contacts = {
					'time' : ball_ball_contacts['time'],
					'collidors' : wall_ball_contacts['collidors']+ball_ball_contacts['collidors'],
				}
			elif ball_ball_contacts['time'] < wall_ball_contacts['time']:
				first_contacts = ball_ball_contacts
			else:
				first_contacts = wall_ball_contacts

		if ball_ball_contacts and not wall_ball_contacts:
			first_contacts = ball_ball_contacts

		if not ball_ball_contacts and wall_ball_contacts:
			first_contacts = wall_ball_contacts

		return first_contacts

	def first_ball_contacts(self, timestep):
		"""Returns the time and all touching ballpairs (ball_1, ball_2) at the time of the first ball-ball collision within the timestep"""
		
		first_ball_contacts = {'time': timestep, 'collidors': []} # collidors will be Ball
		
		for ball_1, ball_2 in itertools.combinations(self.balls, 2):
			
			t = self.collision_time(ball_1, ball_2, timestep)
			if t!=None:
				if t < first_ball_contacts['time']:
						
					first_ball_contacts['time'] = t
					first_ball_contacts['collidors'] = [(ball_1, ball_2)]

				elif t == first_ball_contacts['time']:

					first_ball_contacts['collidors'].append((ball_1, ball_2))

		if not first_ball_contacts['collidors']:
			return None

		return first_ball_contacts

	def first_wall_contacts(self, timestep):
		"""Returns the time, ball_1 and ball_2 of the first ball-wall collision within the timestep. 
		Returns None if there is no contact."""
		
		#Find the first collision with a ball and a wall.
		first_wall_contacts = {'time': timestep, 'collidors': []} # Collidors will be Ball and Wall

		#For the balls that have a positive vy
		for ball in filter(lambda x: x.vy>0, self.balls):
			t = self.time_to_y(ball, self.height-ball.r)
			if t < first_wall_contacts['time']: 
				first_wall_contacts['time'] = t
				first_wall_contacts['collidors'] = [(ball,self.walls[1])] 
			elif t == first_wall_contacts['time']:
				first_wall_contacts['collidors'].append((ball, self.walls[1]))

		#For the balls that have a positive vx
		for ball in filter(lambda x: x.vx>0, self.balls):
			t = self.time_to_x(ball, self.width-ball.r)
			if t < first_wall_contacts['time']: 
				first_wall_contacts['time'] = t
				first_wall_contacts['collidors'] = [(ball,self.walls[2])] 
			elif t == first_wall_contacts['time']:
				first_wall_contacts['collidors'].append((ball, self.walls[2]))

		#For the balls that have a negative vy
		for ball in filter(lambda x: x.vy<0, self.balls):
			t = self.time_to_y(ball, 0+ball.r)
			if t < first_wall_contacts['time']: 
				first_wall_contacts['time'] = t
				first_wall_contacts['collidors'] = [(ball,self.walls[3])] 
			elif t == first_wall_contacts['time']:
				first_wall_contacts['collidors'].append((ball, self.walls[3]))

		#For the balls that have negative vx
		for ball in filter(lambda x: x.vx<0, self.balls):
			t = self.time_to_x(ball, 0+ball.r)
			if t < first_wall_contacts['time']: 
				first_wall_contacts['time'] = t
				first_wall_contacts['collidors'] = [(ball,self.walls[4])] 
			elif t == first_wall_contacts['time']:
				first_wall_contacts['collidors'].append((ball, self.walls[4]))
		
		if not first_wall_contacts['collidors']:
			return None

		return first_wall_contacts

	def progress_balls(self, time):
		for ball in self.balls:
			self.progress_ball(ball, time)
		self.time_elapsed += time

	def progress_ball(self, ball, time): # time is not necessarily timestep
		ball.x = ball.x + ball.vx*time
		ball.y = ball.y + ball.vy*time

	def time_to_x(self, ball, x):
		t = (x-ball.x)/ball.vx
		if t < 0:
			raise NegativeTimeError('function returned a negative time')
		return t

	def time_to_y(self, ball, y):
		t = (y-ball.y)/ball.vy
		if t < 0:
			raise NegativeTimeError('function returned a negative time')
		return t

	def collision_time(self, ball_1, ball_2, time):
		"""Returns collision time if ball_1 and ball_2 collide within time, None if not"""
		t_collide = self.t_collision(ball_1, ball_2)
		
		if t_collide == None:
			return None
		elif t_collide <= time:
			return t_collide
		else:
			return None

	def d_min(self, ball_1, ball_2):
		"""Returns the smallest distance between 
		ball_1 and ball_2 from now (0) to self.timestep"""

		delta_x = ball_1.x - ball_2.x
		delta_y = ball_1.y - ball_2.y # delta_x and delta_y are at the start, before the timestep.
		delta_vx = ball_1.vx - ball_2.vx
		delta_vy = ball_1.vy - ball_2.vy
		
		t_extremum = -((delta_vx*delta_x)+(delta_vy*delta_y))/((delta_vx)**2+(delta_vy)**2) # This is the max or min point. Take note: It's not neccesarily the biggest/smallest distance between the balls during the timestep.
		d_extremum = sqrt((t_extremum*delta_vx+delta_x)**2 + (t_extremum*delta_vy+delta_y)**2) # the distance at t_extremum		

		d_start = norm([delta_x, delta_y]) # The distance at the start of the timestep

		d_timestep = sqrt((self.timestep*delta_vx+delta_x)**2 + (self.timestep*delta_vy+delta_y)**2) # The distance at the end of the timestep

		return min([d_extremum, d_start, d_timestep]) ## Beware of the special case where d_timestep and d_extremum are the same. In that moment, we cannot be sure that the balls will hit eachother and will have to look for another way to know.

	def t_collision(self, ball_1, ball_2):
		"""Returns the time of collision, if there is one, None if not.
		ball_1 and ball_2 should hold the x and y values for the beginning of the timestep
		when the function is called."""

		d = ball_1.r + ball_2.r
		k = ((ball_1.vy-ball_2.vy)**2+(ball_1.vx-ball_2.vx)**2) ## ball_1 == ball_2??
		l = 2*((ball_1.y-ball_2.y)*(ball_1.vy-ball_2.vy)+(ball_1.x-ball_2.x)*(ball_1.vx-ball_2.vx))
		m = -d**2+(ball_1.y-ball_2.y)**2+(ball_1.x-ball_2.x)**2

		try:
			if (l**2)/(4*k**2)-m/k < 0: # if this is less than zero then the equations for t_collide_1 and t_collide_2 have no real solutions, and there is no collision.
				return None
		except ZeroDivisionError as e: # If this is legitimately zerodivision (k is zero) then we have a special case where two balls are travelling at the same speed in the same direction. There is no collision here, so the function should return None. 
			return None

		t_collide_1 = -l/(k*2)+sqrt((l**2)/(4*k**2)-m/k)
		t_collide_2 = -l/(k*2)-sqrt((l**2)/(4*k**2)-m/k)
		
		t_collision = tuple(filter(lambda x: x>=0,(t_collide_1, t_collide_2)))
		
		if t_collision:
			min_t = min(t_collision)

			if isclose(min_t, 0, abs_tol = 0.003):
				v1 = ball_1.vxy_to_vnt(ball_2)
				v2 = ball_2.vxy_to_vnt(ball_1)
				v1_normal = v1[0]
				v2_normal = v2[0]
				if ball_1.derivative(ball_2) >= 0:  ## Exit function if there will be no collision
					return None

			return min_t

		return None

	def stop(self):
		pass

	def start(self):
		pass

	def ball_within_walls(self, r, x, y):
		if x+r <= self.width and y+r <= self.height and x-r >= 0 and y-r >= 0:
			return True
		return False

	def overlap_new_ball(self, new_radius, new_x, new_y): 
		"""	Takes a ball and returns true if its area overlaps 
			with any other ball currently on the board
		"""
		for ball in self.balls:
			
			delta_vector = subtract([new_x,new_y], [ball.x, ball.y])
			distance = norm(delta_vector)
			
			if distance < ball.r+new_radius:

				return True

		return False

	def check_board_for_overlap(self):
		"""Raises an exception if any balls overlap on the board"""
		for ball_1, ball_2 in combinations(self.balls, 2):
			if norm([ball_1.x-ball_2.x, ball_1.y-ball_2.y]) < ball_1.radius + ball_2.radius:
				raise OverlapError

	def get_fastest_ball(self):
		return max(map(lambda x: x.self, self.ball_list))

	def opposite_vectors(self, ball): # Useless function. Collisions can occur between balls travelling in the same direction.
		"""Returns all vectors with at least one velocity component with an opposite sign to that of ball."""
		other_balls = list(filter(lambda x: x!=ball, self.ball_list)) # all except ball
		opposite_vectors = set(filter(lambda x: x.positive_x() != ball.positive_x() or x.positive_y() != ball.positive_y(), other_balls))
		return opposite_vectors

class Ball:

	def __init__(self, parent, xpos = 50, ypos = 50, radius = 100, vx = 0, vy = 0, mass = 1):
		"""
		x,y are positions
		vx and vy are velocities in cells/second
		"""
		self.x = xpos
		self.y = ypos
		self.r = radius
		self.vx = vx
		self.vy = vy
		self.mass = mass
		self.board = parent

	def __str__(self):
		return self._str__()

	__repr__ = __str__

	def _str__(self):
		return "Ball: x={0}, y={1}, r={2}, vx={3}, vy={4}".format(self.x,self.y,self.r,self.vx,self.vy)

	def override_str(self, func): ## Needs testing
		self.__str__ = func	

	def collide(self, other):
		if isinstance(other, Wall):
			self.collide_with_wall(other)
		elif isinstance(other, Ball):
			self.collide_with_ball(other)
		else:
			raise ArgumentError("Invalid type for argument 'other': "+str(type(other)))

	def collide_with_wall(self, wall):

		x = self.x 
		y = self.y # Coordinates of the ball

		if wall.orientation == 1:        ## If there will be no collision, 
			if self.vy <= 0: return  	 # exit function without making 
										 # any changes to the velocity
		elif wall.orientation == 2:      # vector of the ball
			if self.vx <= 0: return 	 
		
		elif wall.orientation == 3:
			if self.vy >= 0: return
		
		elif wall.orientation == 4:
			if self.vx >= 0: return

		else:
			raise WallOrientationError('wall.orientation is holding an invalid value: '+str(wall.orientation))

		switch = {
			1 : 'self.vy = -self.vy' if isclose(y+self.r, self.board.height, abs_tol= ERROR_TOL) else 'raise ProximityError("The absolute value of the distance between ball and wall is too great, error = "+str(y+self.r - self.board.height))',
			2 : 'self.vx = -self.vx' if isclose(x+self.r, self.board.width, abs_tol=ERROR_TOL) else 'raise ProximityError("The absolute value of the distance between ball and wall is too great, error = "+str(y+self.r - self.board.height))',
			3 : 'self.vy = -self.vy' if isclose(y-self.r, 0, abs_tol=ERROR_TOL) else 'raise ProximityError("The absolute value of the distance between ball and wall is too great, error = "+str(y+self.r - self.board.height))',
			4 : 'self.vx = -self.vx' if isclose(x-self.r, 0, abs_tol=ERROR_TOL) else 'raise ProximityError("The absolute value of the distance between ball and wall is too great, error = "+str(y+self.r - self.board.height))',
		}

		exec(switch.get(wall.orientation))

	def vxy_to_vnt(self, other_ball):
		"""Take a vector (x,y) and transforms it to (n,t)-base for the touching point of self and other_ball."""

		r1 = self.r
		r2 = other_ball.r

		if not isclose(self.distance_to(other_ball), r1+r2, abs_tol = ERROR_TOL):
			raise ProximityError("The absolute value of the distance between the two balls is greater than allowed by 'collision()'")

		x2 = other_ball.x 	## In the moment of collision
		x1 = self.x 	## ---||----
		y2 = other_ball.y 	## ---||----
		y1 = self.y 	## ---||----
		v1 = np.array([[self.vx],[self.vy]])

		ct = np.array([
			[x2-x1, y2-y1],
			[y2-y1, x2-x1],
			])/(r1+r2)
		ct_inv = np.array([ # The inverse of ct
			[x2-x1, y2-y1],
			[y2-y1, x2-x1],
			])*((r1+r2)/((x2-x1)**2-(y2-y1)**2))

		return np.dot(ct_inv, v1) # This vector now contains the scalars for the unit vectors in normal and tangent direction of the collision line between the two balls.

	def collide_with_ball(self, other_ball):
		r1 = self.r
		r2 = other_ball.r

		if not isclose(self.distance_to(other_ball), r1+r2, abs_tol = ERROR_TOL):
			raise ProximityError("The absolute value of the distance between the two balls is greater than allowed.")

		if self.derivative(other_ball)>=0: # If the derivative of the distance between 
			return 						  # the centers of gravity at the time of 
										  # contact is positive, the balls are
										  # moving apart and the is no collision.

		x2 = other_ball.x 	## In the moment of collision
		x1 = self.x 	## ---||----
		y2 = other_ball.y 	## ---||----
		y1 = self.y 	## ---||----
		v1 = [self.vx, self.vy]
		v2 = [other_ball.vx, other_ball.vy]
		m1 = self.mass
		m2 = other_ball.mass
		
		n = [x2-x1,y2-y1]
		un = np.divide(n,norm(n))
		ut = [-un[1], un[0]]

		v1n = np.dot(un, v1)
		v1t = np.dot(ut, v1)
		v2n = np.dot(un, v2)
		v2t = np.dot(ut, v2)

		v1t_prime_scalar = v1t
		v2t_prime_scalar = v2t

		v1n_prime_scalar = (v1n*(m1-m2) + 2*m2*v2n)/(m1+m2)
		v2n_prime_scalar = (v2n*(m2-m1) + 2*m1*v1n)/(m1+m2)

		v1n_prime = np.multiply(v1n_prime_scalar, un)
		v1t_prime = np.multiply(v1t_prime_scalar, ut)

		v2n_prime = np.multiply(v2n_prime_scalar, un)
		v2t_prime = np.multiply(v2t_prime_scalar, ut)

		v1_prime = np.add(v1n_prime, v1t_prime)
		v2_prime = np.add(v2n_prime, v2t_prime) 

		self.vx = v1_prime[0]
		self.vy = v1_prime[1]
		other_ball.vx = v2_prime[0]
		other_ball.vy = v2_prime[1]

	def old_collide_with_ball(self, other_ball): ## IS NOT USED ANYMORE
		"""changes the velocities for self and other_ball in a collision. Must only be run on touching balls."""
		
		if self.derivative(other_ball)>0: # If the derivative of the distance between 
			return 						  # the centers of gravity at the time of 
										  # contact is positive, the balls are
										  # moving apart and the is no collision.

		r1 = self.r
		r2 = other_ball.r

		if not isclose(self.distance_to(other_ball), r1+r2, abs_tol = ERROR_TOL):
			raise ProximityError("The absolute value of the distance between the two balls is greater than allowed by 'collision()'")

		x2 = other_ball.x 	## In the moment of collision
		x1 = self.x 	## ---||----
		y2 = other_ball.y 	## ---||----
		y1 = self.y 	## ---||----
		v1 = np.array([[self.vx],[self.vy]])
		v2 = np.array([[other_ball.vx],[other_ball.vy]])
		m1 = self.mass
		m2 = other_ball.mass

		v1_after = None
		v2_after = None

		ct = np.array([
			[x2-x1, y2-y1],
			[y2-y1, x2-x1],
			])/(r1+r2)
		ct_inv = np.array([ # The inverse of ct
			[x2-x1, y2-y1],
			[y2-y1, x2-x1],
			])*((r1+r2)/((x2-x1)**2-(y2-y1)**2))

		v1_transform = np.dot(ct_inv, v1)
		v2_transform = np.dot(ct_inv, v2) # These vectors now contain the scalars for the unit vectors in normal and tangent direction of the collision line between the two balls.

		v1_normal = v1_transform[0]
		v2_normal = v2_transform[0]
		v1_tangent = v1_transform[1]
		v2_tangent = v2_transform[1]



		if abs(v1_normal + v2_normal) == abs(v1_normal)+abs(v2_normal):  ## Exit function if there will be no collision
			return ## This needs to be tested. ##COULD BE BUG
		## Calculating the velocity after collision

		u1_normal = (m1-m2)/(m1+m2)*v1_normal + 2*m2/(m1+m2)*v2_normal
		u2_normal = 2*m1/(m1+m2)*v1_normal + (m1-m2)/(m1+m2)*v2_normal # According to the formula for head on elastic collision
		u1_tangent = v1_tangent
		u2_tangent = v2_tangent  # Because the tangent component is unchanged

		u1_transform = [u1_normal, u1_tangent]
		u2_transform = [u2_normal, u2_tangent]
		
		u1 = np.dot(ct, u1_transform)
		u2 = np.dot(ct, u2_transform)

		## Setting the new velocities

		self.vx = u1[0][0]
		self.vy = u1[1][0]
		other_ball.vx = u2[0][0]
		other_ball.vy = u2[1][0] # Testing showed that changing all the signs was necessary. There must be some kind of algebraic fault in the computations above.

	def positive_x(self):
		"""Returns True if vx i positive, False if negative, -1 if 0."""
		if self.v_vector[0] > 0:
			return True
		elif self.v_vector[0] < 0:
			return False
		else: 
			raise ZeroError()

	def positive_y(self):
		"""Returns 1 if vy is positive, 0 otherwise."""
		if self.v_vector[1] > 0:
			return True
		elif self.v_vector[1] < 0:
			return False
		else:
			raise ZeroError()

	def distance_to(self, other_ball):
		return norm([
			self.x - other_ball.x,
			self.y - other_ball.y,
			])

	def derivative(self, other_ball):
		"""
		Returns the derivative of the squared distance between self and other_ball (pythagoras theorem d^2 = delta_x^2 + delta_y^2) with respect to time.
		"""
		x1_0 = self.x
		x2_0 = other_ball.x
		y1_0 = self.y
		y2_0 = other_ball.y
		v1_x = self.vx
		v2_x = other_ball.vx
		v1_y = self.vy
		v2_y = other_ball.vy
		t = 0

		d_prime = 2*(x1_0-x2_0+t*(v1_x-v2_x))*(v1_x-v2_x)+2*(y1_0-y2_0+t*(v1_y-v2_y))*(v1_y-v2_y)

		return d_prime

class MoveableBall(Ball):
	def __init__(self, parent, xpos = 50, ypos = 50, radius = 100, vx = 0, vy = 0, mass = 1, delta_vx = 0, delta_vy = 0):
		super().__init__(self, parent, xpos = 50, ypos = 50, radius = 100, vx = 0, vy = 0, mass = 1)
		self.delta_vx = delta_vx # This is the value that will be added to vx in the next timestep
		self.delta_vy = delta_vy # dito for vy



class Wall():
	def __init__(self, parent, orientation):
		"""
		Orientation: 
			1 = Top
			2 = Right
			3 = Bottom
			4 = Left
		length: The length of the wall
		constant_coord: the coordinate which is constant in a wall that lies straight along the x or y axes.
		"""
		if not (orientation in (1,2,3,4)):
			raise ArgumentError('Orientation of wall must be a number in (1, 2, 3, 4)')

		if not isinstance(parent, Board):
			raise ArgumentError('Parent must be instance of class Board')

		self.orientation = orientation
		self.board = parent

		switch = {
			1: 'self.y = parent.height',
			2: 'self.x = parent.width',
			3: 'self.y = 0',
			4: 'self.x = 0',
		}
		exec(switch.get(orientation))
	
	def collide(self, other):
		if isinstance(other, Ball):
			other.collide_with_wall(self)
		else:
			raise ArgumentError('Only ball objects can collide with walls.')

	def __str__(self):
		return "Wall "+str(self.orientation)
	
	__repr__ = __str__

class Coords():
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Collisions(): ## Seems useless as of now
	"""Meant to store a group of objects that will collide at the same time, 
	in pairs, and return them one by one for Board to call collision for 
	them. The iterable should give each successive pair of colliding objects 
	that the new speeds should be calculated for."""
	def __init__(self, colliding_balls):
		self.ball_pairs = colliding_balls
		self.started = False
	def order(self):
		dict = {}
	def __iter__(self):
		self.order()
		yield self.ball_pair[0]
		if self.started:
			pass
		else:
			pass