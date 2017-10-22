import unittest

from model.boardmodel import Board, Ball, Wall
from model.exceptions.exceptions import ProximityError

class BoardModelMethods(unittest.TestCase):

	def assertRaisesWithMessage(self, msg, func, *args, **kwargs):
		try:	
			func(*args, **kwargs)
			self.assertFail()
		except Exception as inst:
			self.assertEqual(inst.message, msg)

	def test_collide_ball_wall(self):
		board = Board(width = 100, height = 100, sps = 2)
		
		ball = board.add_ball(x = 50, y = 90, r = 10, vx = 0, vy = 1, m = 1)
		ball.collide(Wall(board, 1)) # Collide with upper wall
		self.assertEqual(ball.vx, 0) # Should be unchanged
		self.assertEqual(ball.vy, -1) # Should be inverted

		ball = board.add_ball(x = 90, y = 50, r = 10, vx = 1, vy = 1, m = 1)
		ball.collide(Wall(board, 2)) # Collide with right wall
		self.assertEqual(ball.vx, -1) # Should be inverted
		self.assertEqual(ball.vy, 1) # Should be unchanged

		ball = board.add_ball(x = 50, y = 10, r = 10, vx = 1, vy = -1, m = 1)
		ball.collide(Wall(board, 3)) # Collide with bottom wall
		self.assertEqual(ball.vx, 1) # Should be unchanged
		self.assertEqual(ball.vy, 1) # Should be inverted
		
		ball = board.add_ball(x = 10, y = 50, r = 10, vx = -1, vy = 1, m = 1)
		ball.collide(Wall(board, 4)) # Collide with left wall
		self.assertEqual(ball.vx, 1) # Should be inverted
		self.assertEqual(ball.vy, 1) # Should be unchanged

		with self.assertRaises(ProximityError):
			ball = board.add_ball(x = 50, y = 50, r = 10, vx = 1, vy = 1, m = 1)
			ball.collide(Wall(board, 1)) # This shouldn't work


	def test_collide_ball_ball(self):

		board = Board(width = 100, height = 100)
		ball_1 = board.add_ball(x = 45, y = 50, r = 5, vx = 2, vy = 0, m = 1)
		ball_2 = board.add_ball(x = 55, y = 50, r = 5, vx = -2, vy = 0, m = 1)

		ball_1.collide(ball_2)

		self.assertEqual(ball_1.x, 45)
		self.assertEqual(ball_2.x, 55)
		self.assertEqual(ball_1.y, 50)
		self.assertEqual(ball_2.y, 50)

		self.assertEqual(ball_1.r, 5)
		self.assertEqual(ball_2.r, 5)

		self.assertEqual(ball_1.vx, -2)
		self.assertEqual(ball_2.vx, 2)
		self.assertEqual(ball_1.vy, 0)
		self.assertEqual(ball_2.vy, 0)


		board = Board(width = 100, height = 100) # Same thing with one line changed
		ball_1 = board.add_ball(x = 45, y = 50, r = 5, vx = 2, vy = 0, m = 1)
		ball_2 = board.add_ball(x = 55, y = 50, r = 5, vx = -2, vy = 0, m = 1)

		ball_2.collide(ball_1) # This line is changed

		self.assertEqual(ball_1.x, 45)
		self.assertEqual(ball_2.x, 55)
		self.assertEqual(ball_1.y, 50)
		self.assertEqual(ball_2.y, 50)

		self.assertEqual(ball_1.r, 5)
		self.assertEqual(ball_2.r, 5)

		self.assertEqual(ball_1.vx, -2)
		self.assertEqual(ball_2.vx, 2)
		self.assertEqual(ball_1.vy, 0)
		self.assertEqual(ball_2.vy, 0)


		board = Board(width = 100, height = 100) # Testing something not as straight and not as symmetrical...
		ball_1 = board.add_ball(x = 50, y = 45, r = 5, vx = 2, vy = 1, m = 1)
		ball_2 = board.add_ball(x = 50, y = 55, r = 5, vx = -2, vy = -10, m = 1)

		ball_1.collide(ball_2)

		self.assertEqual(ball_1.vx, 2.0)
		self.assertEqual(ball_2.vx, -2.0)
		self.assertEqual(ball_1.vy, -10.0)
		self.assertEqual(ball_2.vy, 1.0)

		board = Board(width = 100, height = 100) # Same thing with one line changed
		ball_1 = board.add_ball(x = 50, y = 55, r = 5, vx = 0, vy = -1, m = 1)
		ball_2 = board.add_ball(x = 50, y = 45, r = 5, vx = 0, vy = 1, m = 1)

		ball_1.collide(ball_2)

		self.assertEqual(ball_1.vy, 1)
		self.assertEqual(ball_2.vy, -1)

		######################################################################
		# Starting with two balls with distance bewtween them. Letting 
		# them get closer with two step()-calls so that they are 
		# touching. Then test the collide function, because they're 
		# touching now.
		SCREEN_RES = {'width':1100, 'height':800}
		board = Board(**SCREEN_RES)
		ball_1 = board.add_ball(r = 100, x = 480, y = 600, vx = 10, vy = 0, m = 23)
		ball_2 = board.add_ball(r = 100, x = 700, y = 600, vx = -10, vy = 0, m = 23)

		board.step()

		self.assertEqual(ball_1.x, 485)
		self.assertEqual(ball_2.x, 695)
		self.assertEqual(ball_1.y, 600)
		self.assertEqual(ball_2.y, 600)

		board.step()

		self.assertEqual(ball_1.x, 490)
		self.assertEqual(ball_2.x, 690)
		self.assertEqual(ball_1.y, 600)
		self.assertEqual(ball_2.y, 600)

		ball_1.collide(ball_2)

		self.assertEqual(ball_1.vx, -10)
		self.assertEqual(ball_1.vy, 0)
		self.assertEqual(ball_2.vx, 10)
		self.assertEqual(ball_2.vy, 0)

		######################################################################
		# Starting with 4 balls touching and one colliding with them.
		# 
		# 
		# 
		print("\n\nStarting the 5-way collision test\n\n")
		SCREEN_RES = {'width':1100, 'height':800}
		board = Board(**SCREEN_RES, slow = True)
		ball_1 = board.add_ball(r=10, x = 500, y=500, vx=0,vy=0)
		ball_2 = board.add_ball(r=10, x=520, y=500, vx=0, vy=0)
		ball_3 = board.add_ball(r=10, x = 500, y=520, vx = 0, vy=0)
		ball_4 = board.add_ball(r=10, x = 520, y=520, vx=0,vy=0)

		ball_5 = board.add_ball(r=10, x=510, y=481, vx=0, vy=1)

		def func_factory(string):
			def func():
				return string
			return func

		ball_1._str__ = func_factory("Bottom Left")
		ball_2._str__ = func_factory("Bottom Right")
		ball_3._str__ = func_factory("Top Left")
		ball_4._str__ = func_factory("Top Right")
		ball_5._str__ = func_factory("Comet")

		board.step()

		self.assertEqual(ball_5.y, 481.5)

		board.step()

		self.assertEqual(ball_5.y, 482)

		board.step()

		self.assertEqual(ball_5.y, 482.5)

		board.step()

		self.assertEqual(ball_5.y, 483)


	def test_get_balls_pygame(self):
		########################################################################
		board = Board(width = 100, height = 100)
		board.add_ball(r=1, x = 50, y = 50, vx = 10, vy = 10)
		pygame_balls = board.get_balls_pygame()

		for ball in pygame_balls:
			for val in ball.values():
				self.assertIsInstance(val, int)

		self.assertEqual(pygame_balls, [{'r':1, 'x':50, 'y':50}])

		del board

		########################################################################
		board = Board(width = 100, height = 100, sps = 1)

		ball_1 = board.add_ball(x = 10, y = 10, r = 5, vx = 2, vy = 2, m = 1)
		ball_2 = board.add_ball(x = 50, y = 50, r = 5, vx = -2, vy = -2, m = 1)

		board.step()
		self.assertEqual(board.time_elapsed, 1)

		self.assertEqual(ball_1.x, 12)
		self.assertEqual(ball_1.y, 12)
		self.assertEqual(ball_2.x, 48)
		self.assertEqual(ball_2.y, 48)
		balls = board.get_balls_pygame()
		self.assertEqual(len(balls), len(board.get_ball_list()))

		pygame_balls = board.get_balls_pygame()
		ball_list = board.get_ball_list()

		for ball in pygame_balls:
			for val in ball.values():
				self.assertIsInstance(val, int)


		for r in map(lambda x: x['r'], pygame_balls):
			self.assertIn(r, map(lambda x: x.r, ball_list))

		for x in map(lambda x: x['x'], pygame_balls):
			self.assertIn(x, map(lambda x: x.x, ball_list))

		for y in map(lambda x: x['y'], pygame_balls):
			self.assertIn(x, map(lambda x: x.y, ball_list))

	def test_step_without_balls(self):
		board = Board(width = 100, height = 100, sps = 1)

		#Take step without balls
		board.step()
		#Test that time is progressed by a timestep
		self.assertEqual(board.time_elapsed, 1)
		
	def test_step_with_balls(self):
		board = Board(width = 100, height = 100, sps = 1)

		ball_1 = board.add_ball(x = 10, y = 10, r = 5, vx = 2, vy = 2, m = 1)
		ball_2 = board.add_ball(x = 50, y = 50, r = 5, vx = -2, vy = -2, m = 1)

		board.step()
		self.assertEqual(board.time_elapsed, 1)

		self.assertEqual(ball_1.x, 12)
		self.assertEqual(ball_1.y, 12)
		self.assertEqual(ball_2.x, 48)
		self.assertEqual(ball_2.y, 48)
		balls = board.get_balls_pygame()
		self.assertEqual(len(balls), len(board.get_ball_list()))

		SCREEN_RES = {'width':1100, 'height':800}
		board = Board(**SCREEN_RES)
		ball_1 = board.add_ball(r = 100, x = 900, y = 600, vx = 20, vy = 0, m = 23)
		ball_2 = board.add_ball(r=50, x = 600, y = 400, vx = 40, vy = -20, m = 10)

		board.step()
		
		self.assertEqual(ball_1.x, 900+ball_1.vx*board.timestep)
		self.assertEqual(ball_2.x, 600+ball_2.vx*board.timestep)

	def test_step_with_touching_but_not_colliding_balls(self):
		## balls will not collide, but they will touch in the first moment.
		## The problem here is that they are listed as touching with time 0,
		## and thus the loop in step() is never exited.
		SCREEN_RES = {'width':1100, 'height':800}
		board = Board(**SCREEN_RES)
		ball_1 = board.add_ball(r = 100, x = 500, y = 600, vx = 20, vy = 0, m = 23)
		ball_2 = board.add_ball(r=50, x = 650, y = 600, vx = 40, vy = 0, m = 10)

		board.step()

		self.assertEqual(ball_1.x, 500+ball_1.vx*board.timestep)
		self.assertEqual(ball_1.y, 600+ball_1.vy*board.timestep)
		self.assertEqual(ball_2.x, 650+ball_2.vx*board.timestep)
		self.assertEqual(ball_2.y, 600+ball_2.vy*board.timestep)

		#########################################################################
		# We continue on the same setup.
		board.step()

		self.assertEqual(ball_1.x, 500+2*ball_1.vx*board.timestep)
		self.assertEqual(ball_1.y, 600+2*ball_1.vy*board.timestep)
		self.assertEqual(ball_2.x, 650+2*ball_2.vx*board.timestep)
		self.assertEqual(ball_2.y, 600+2*ball_2.vy*board.timestep)

		for i in range(24):
			board.step()

	def test_step_colliding_balls_from_distance(self):
		SCREEN_RES = {'width':1100, 'height':800}
		board = Board(**SCREEN_RES)
		ball_1 = board.add_ball(r = 100, x = 480, y = 600, vx = 10, vy = 0, m = 23)
		ball_2 = board.add_ball(r = 100, x = 700, y = 600, vx = -10, vy = 0, m = 23)

		board.step()

		self.assertEqual(ball_1.x, 485)
		self.assertEqual(ball_2.x, 695)
		self.assertEqual(ball_1.y, 600)
		self.assertEqual(ball_2.y, 600)

		board.step()

		self.assertEqual(ball_1.x, 490)
		self.assertEqual(ball_2.x, 690)
		self.assertEqual(ball_1.y, 600)
		self.assertEqual(ball_2.y, 600)

		board.step()

		######################################################################
		# Trying an example where the balls aren't touching before the collision 
		# but will do so during timestep
		# 
		# 
		board = Board(width = 100, height = 100, sps = 2)
		ball_1 = board.add_ball(r = 1, x = 45, y = 50, vx = 5, vy = 0, m = 23)
		ball_2 = board.add_ball(r = 1, x = 50, y = 50, vx = -5, vy = 0, m = 23)

		board.step()
		board.step()
		board.step()

	def test_step_y_direction(self):
		#######################################################################
		# collision from above

		board = Board(width = 1000, height = 1000)
		ball_1 = board.add_ball(r = 10, x = 500, y = 500, vx = 0, vy = -5, m = 23)
		ball_2 = board.add_ball(r = 10, x = 500, y = 450, vx = 0, vy = 5, m = 23)

		for i in range(4):
			board.step()

	def test_add_ball(self):
		board = Board(width = 100, height = 100, sps = 1)

		ball_1 = board.add_ball(x = 10, y = 10, r = 5, vx = 2, vy = 2, m = 1)

		self.assertEqual(ball_1, board.get_ball_list()[0])

	def test_progress_balls(self):
		board = Board(width = 100, height = 100, sps = 1)

		ball_1 = board.add_ball(x = 10, y = 10, r = 5, vx = 2, vy = 2, m = 1)
		ball_2 = board.add_ball(x = 50, y = 50, r = 5, vx = -2, vy = -2, m = 1)

		board.progress_balls(2)

		self.assertEqual(ball_1.x, 14)
		self.assertEqual(ball_1.y, 14)

		self.assertEqual(ball_2.x, 46)
		self.assertEqual(ball_2.y, 46)

	def test_collide_wall_1(self):
		board = Board(width = 100, height = 100, sps = 1)
		ball = board.add_ball(x = 50, y = 70, r = 10, vx = 0, vy = 1, m = 1)

		for i in range(20):
			board.step()

		self.assertEqual(ball.y, 90)

		board.step()

		self.assertEqual(ball.y, 89)

	def test_collide_wall_2(self):
		board = Board(width = 1000, height = 1000, sps = 1)
		ball = board.add_ball(x = 800, y = 100, r = 100, vx = 10, vy = 0, m = 1)		

		for i in range(10):
			board.step()

		self.assertEqual(ball.x, 900)

		board.step()

		self.assertEqual(ball.x, 890)

	def test_collide_wall_3(self):
		board = Board(width = 1000, height = 1000, sps = 1)
		ball = board.add_ball(x = 500, y = 200, r = 100, vx = 0, vy = -10, m = 1)

		for i in range(10):
			board.step()

		self.assertEqual(ball.y, 100)

		board.step()

		self.assertEqual(ball.y, 110)

	def test_collide_wall_4(self):
		board = Board(width = 1000, height = 1000, sps = 1)
		ball = board.add_ball(x = 200, y = 500, r = 100, vx = -10, vy = 0, m = 1)

		for i in range(10):
			board.step()

		self.assertEqual(ball.x, 100)

		board.step()

		self.assertEqual(ball.x, 110)

	def test_first_wall_contacts_wall_1(self):
		## ball is touching wall
		board = Board(width = 100, height = 100, sps = 1)
		ball = board.add_ball(x = 50, y = 90, r = 10, vx = 0, vy = 1, m = 1)

		contacts = board.first_wall_contacts(1)

		collidors = contacts['collidors']

		self.assertEqual(collidors, [(ball,board.walls[1])])


	def test_first_wall_contacts_wall_2(self):
		## ball is touching wall
		board = Board(width = 100, height = 100, sps = 1)
		ball = board.add_ball(x = 90, y = 50, r = 10, vx = 1, vy = 0, m = 1)
		contacts = board.first_wall_contacts(1)

		collidors = contacts['collidors']

		self.assertEqual(collidors, [(ball,board.walls[2])])

	def test_first_wall_contacts_wall_3(self):
		## ball is touching wall
		board = Board(width = 100, height = 100, sps = 1)
		ball = board.add_ball(x = 50, y = 10, r = 10, vx = 0, vy = -1, m = 1)

		contacts = board.first_wall_contacts(1)

		collidors = contacts['collidors']

		self.assertEqual(collidors, [(ball,board.walls[3])])

	def test_first_wall_contacts_wall_4(self):
		## ball is touching wall
		board = Board(width = 100, height = 100, sps = 1)
		ball = board.add_ball(x = 10, y = 50, r = 10, vx = -1, vy = 0, m = 1)

		contacts = board.first_wall_contacts(1)

		collidors = contacts['collidors']

		self.assertEqual(collidors, [(ball,board.walls[4])])

	def test_first_wall_contacts_no_contact_with_wall(self):

		SCREEN_RES = {'width':1100, 'height':800}
		board = Board(**SCREEN_RES)
		ball_1 = board.add_ball(r = 100, x = 500, y = 600, vx = 20, vy = 0, m = 23)
		ball_2 = board.add_ball(r = 50, x = 650, y = 600, vx = 40, vy = 0, m = 10)

		wall_contacts = board.first_wall_contacts(1)

		self.assertEqual(wall_contacts, None)
		self.assertEqual(wall_contacts, None)

	def test_first_ball_contacts_2_balls(self):

		board = Board(width = 100, height = 100, sps = 1) # Same thing with one line changed
		ball_1 = board.add_ball(x = 45, y = 50, r = 5, vx = 2, vy = 0, m = 1)
		ball_2 = board.add_ball(x = 55, y = 50, r = 5, vx = -2, vy = 0, m = 1)

		contacts = board.first_ball_contacts(1)
		self.assertEqual(contacts['time'], 0)
		self.assertEqual(len(contacts['collidors'][0]), 2)
		self.assertEqual(board.get_ball_list(), list(contacts['collidors'][0]))

		balls = board.get_balls_pygame()
		self.assertEqual(len(balls), 2)

		###################################################################
		SCREEN_RES = {'width':1100, 'height':800}
		board = Board(**SCREEN_RES)
		ball_1 = board.add_ball(r = 100, x = 500, y = 600, vx = 20, vy = 0, m = 23)
		ball_2 = board.add_ball(r = 50, x = 650, y = 600, vx = 40, vy = 0, m = 10)
	
		contacts = board.first_ball_contacts(board.timestep)
		self.assertEqual(contacts, None)


	def test_collision_time(self):
		board = Board(width = 100, height = 100, sps = 1) # Same thing with one line changed
		ball_1 = board.add_ball(x = 45, y = 50, r = 5, vx = 2, vy = 0, m = 1)
		ball_2 = board.add_ball(x = 55, y = 50, r = 5, vx = -2, vy = 0, m = 1)

		tc = board.t_collision(ball_1, ball_2)

		t = board.collision_time(ball_1, ball_2, 1)
		self.assertEqual(t, 0)
		
		###################################################################
		SCREEN_RES = {'width':1100, 'height':800}
		board = Board(**SCREEN_RES)
		ball_1 = board.add_ball(r = 100, x = 500, y = 600, vx = 20, vy = 0, m = 23)
		ball_2 = board.add_ball(r = 50, x = 650, y = 600, vx = 40, vy = 0, m = 10)

		t = board.collision_time(ball_1, ball_2, 1)
		self.assertEqual(t, None)

	def test_t_collision(self):
		board = Board(width = 100, height = 100, sps = 1) # Same thing with one line changed
		ball_1 = board.add_ball(x = 45, y = 50, r = 5, vx = 2, vy = 0, m = 1)
		ball_2 = board.add_ball(x = 55, y = 50, r = 5, vx = -2, vy = 0, m = 1)

		t = board.t_collision(ball_1, ball_2)
		self.assertEqual(t, 0)

		###################################################################
		SCREEN_RES = {'width':1100, 'height':800}
		board = Board(**SCREEN_RES)
		ball_1 = board.add_ball(r = 100, x = 500, y = 600, vx = 20, vy = 0, m = 23)
		ball_2 = board.add_ball(r = 50, x = 650, y = 600, vx = 40, vy = 0, m = 10)

		t = board.t_collision(ball_1, ball_2)
		self.assertEqual(t, None)

	def test_ball__str__(self):
		board = Board()
		ball = Ball(parent = board, xpos = 50, ypos = 50, radius = 100, vx = 0, vy = 0, mass = 1)
		self.assertEqual(str(ball), "Ball: x={0}, y={1}, r={2}, vx={3}, vy={4}".format(ball.x,ball.y,ball.r,ball.vx,ball.vy))





if __name__ == "__main__":
	unittest.main()

