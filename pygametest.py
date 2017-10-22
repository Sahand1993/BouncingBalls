from model.boardmodel import Board

SCREEN_RES = (1100,800)

board = Board()

color = (255,255,255)

def add_balls(board):
	board.add_ball(r = 100, x = 500, y = 400, vx = 100, vy = 100, m = 23)

def disp_balls(board):
	balls = board.get_balls_pygame()
	print(balls)
	for ball in balls:
		center = (ball['x'], ball['y'])
		radius = ball['r']


add_balls(board)
disp_balls(board)