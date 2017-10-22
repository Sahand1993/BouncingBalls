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
		return "Ball: x={0}, y={1}, r={2}, vx={3}, vy={4}".format(self.x,self.y,self.r,self.vx,self.vy)

class Board:
	
	def __init__(self, width = 100, height = 100, sps = 2):
		pass

board = Board()

ball = Ball(board)
ball_list = [Ball(board), Ball(board)]
ball_dict = {'ball_1':Ball(board), 'ball_2':Ball(board)}

print(ball)
print(ball_list)
print(ball_dict)