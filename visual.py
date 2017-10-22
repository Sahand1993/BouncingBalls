import pygame, sys, os
from pygame.locals import *
import model
import time
from threading import Thread
import math

SCREEN_RES = {'width':1300, 'height':800}

pygame.init()

res = tuple(SCREEN_RES.values())

if input("Enter f for FULLSCREEN:") == "f":
	screen = pygame.display.set_mode(res, FULLSCREEN)
else:
	screen = pygame.display.set_mode(res)

board = model.boardmodel.Board(**SCREEN_RES)

color = (255,255,255)

lenne = pygame.image.load("pics/lenne.png")
lenne = pygame.transform.scale(lenne, (100,100))
lenne.convert()

def add_balls1(board):
	board.add_ball(r = 100, x = 900, y = 600, vx = 20, vy = 0, m = 23)
	board.add_ball(r = 50, x = 600, y = 400, vx = 40, vy = -20, m = 23)

def add_balls2(board):
	board.add_ball(r = 100, x = 500, y = 600, vx = 20, vy = 0, m = 23)
	board.add_ball(r = 50, x = 650, y = 600, vx = 40, vy = 0, m = 10)

def add_balls3(board):
	board.add_ball(r = 100, x = 480, y = 600, vx = 10, vy = 0, m = 23)
	board.add_ball(r = 100, x = 700, y = 600, vx = -10, vy = 0, m = 23)

def add_balls4(board):
	ball_1 = board.add_ball(r = 1, x = 45, y = 50, vx = 5, vy = 0, m = 23)
	ball_2 = board.add_ball(r = 1, x = 50, y = 50, vx = -5, vy = 0, m = 23)

def add_balls5(board):
	ball_1 = board.add_ball(r = 10, x = 500, y = 50, vx = 5, vy = 0, m = 23)
	ball_2 = board.add_ball(r = 10, x = 556, y = 50, vx = -5, vy = 0, m = 23)

def add_balls5(board):
	ball_1 = board.add_ball(r = 10, x = 500, y = 550, vx = 5, vy = -5, m = 23)
	ball_2 = board.add_ball(r = 10, x = 580, y = 450, vx = -5, vy = 5, m = 23)

def add_balls6(board):
	ball_1 = board.add_ball(r = 5, x = 50, y = 55, vx = 0, vy = -1, m = 1)
	ball_2 = board.add_ball(r = 5, x = 50, y = 45, vx = 0, vy = 1, m = 1)

def add_balls7(board): #Buggar för width = 1100, height = 800
	ball_1 = board.add_ball(r = 40, x = 900, y = 750, vx = 0, vy = -1, m = 1)
	ball_2 = board.add_ball(r = 5, x = 700, y = 700, vx = 0, vy = 1, m = 1)	
	ball_3 = board.add_ball(r = 50, x = 500, y = 500, vx = 5, vy = 3, m = 100)
	ball_4 = board.add_ball(r=100, x = 100, y = 100, vx = 7, vy = -5, m = 20)
	ball_5 = board.add_ball(r = 5, x = 800, y = 750, vx = 0, vy = -1, m = 1)
	ball_6 = board.add_ball(r = 5, x = 750, y = 700, vx = 0, vy = 1, m = 1)
	ball_7 = board.add_ball(r = 5, x = 800, y = 700, vx = 0, vy = -1, m = 1)
	ball_8 = board.add_ball(r = 5, x = 700, y = 600, vx = 0, vy = 1, m = 1)
	ball_9 = board.add_ball(r = 5, x = 770, y = 600, vx = 0, vy = 1, m = 1)
	ball_9 = board.add_ball(r = 5, x = 790, y = 600, vx = 0, vy = 1, m = 1)
	ball_10 = board.add_ball(r = 5, x = 500, y = 600, vx = 0, vy = 1, m = 1)
	ball_11 = board.add_ball(r = 5, x = 800, y = 660, vx = 0, vy = 1, m = 1)
	ball_12 = board.add_ball(r = 5, x = 700, y = 680, vx = 0, vy = 1, m = 1)
	ball_13 = board.add_ball(r = 5, x = 700, y = 610, vx = 0, vy = 1, m = 1)
	ball_14 = board.add_ball(r = 5, x = 700, y = 620, vx = 0, vy = 1, m = 1)

def add_balls8(board):
	ball_1 = board.add_ball(r=10, x = 500, y=500, vx=0,vy=0)
	ball_2 = board.add_ball(r=10, x=520, y=500, vx=0, vy=0)
	ball_3 = board.add_ball(r=10, x = 520, y=520, vx=0,vy=0)
	ball_5 = board.add_ball(r=10, x=510, y=481, vx=0, vy=1)
	ball_6 = board.add_ball(r=100, x=600, y= 200, vx=2, vy=0, m=100)

def add_balls9(board): #buggar för width = 1300, height = 800
	ball_1 = board.add_ball(r=10, x = 500, y=500, vx=0,vy=0)
	ball_2 = board.add_ball(r=10, x=520, y=500, vx=0, vy=0)
	ball_3 = board.add_ball(r=10, x = 520, y=520, vx=0,vy=0)
	ball_4 = board.add_ball(r=10, x=510, y=451, vx=0, vy=2)

	ball_5 = board.add_ball(r=10, x=400, y=500, vx=0, vy=0)
	ball_6 = board.add_ball(r=10, x=420, y=500, vx=0, vy=0)
	ball_7 = board.add_ball(r=10, x=420, y=520, vx=0, vy=0)
	ball_8 = board.add_ball(r=10, x=410, y=451, vx=0, vy=2)

def add_balls10(board):
	ball_1 = board.add_ball(r=10, x = 500, y=500, vx=0,vy=0)
	ball_2 = board.add_ball(r=10, x=520, y=500, vx=0, vy=0)
	ball_3 = board.add_ball(r=10, x = 520, y=520, vx=0,vy=0)
	ball_4 = board.add_ball(r=10, x = 500, y=520, vx = 0, vy=0)
	ball_5 = board.add_ball(r=10, x=510, y=430, vx=0, vy=1)

def add_balls11(board):
	ball_1 = board.add_ball(r=10, x = 500, y=500, vx=0,vy=0)
	ball_2 = board.add_ball(r=10, x=520, y=500, vx=0, vy=0)
	ball_3 = board.add_ball(r=10, x = 500, y=520, vx = 0, vy=0)
	ball_4 = board.add_ball(r=10, x=510, y=430, vx=0, vy=1)	

	ball_5 = board.add_ball(r=10, x = 600, y=500, vx=0,vy=0)
	ball_6 = board.add_ball(r=10, x=620, y=500, vx=0, vy=0)
	ball_7 = board.add_ball(r=10, x = 620, y=520, vx = 0, vy=0)
	ball_8 = board.add_ball(r=10, x=610, y=430, vx=0, vy=1)	

def add_balls12(board): # all separated by 1
	ball_1 = board.add_ball(r=10, x = 500, y=500, vx=0,vy=0)
	ball_2 = board.add_ball(r=10, x=521, y=500, vx=0, vy=0)

	ball_4 = board.add_ball(r=10, x = 500, y=521, vx = 0, vy=0)
	ball_3 = board.add_ball(r=10, x = 521, y=521, vx=0,vy=0)

	ball_5 = board.add_ball(r=10, x=510, y=430, vx=0, vy=1)	

def add_balls13(board): 
	ball_1 = board.add_ball(r=10, x = 500, y = 500, vx=0, vy=0)
	ball_2 = board.add_ball(r=10, x=500, y=520, vx=0, vy=0)
	ball_3 = board.add_ball(r=10, x=500, y=540, vx=0, vy=0)

	ball_4 = board.add_ball(r=10, x=500, y=400, vx=0, vy=1)


def add_balls14(board): # above two separated by 1
	ball_1 = board.add_ball(r=10, x = 500, y=500, vx=0,vy=0)
	ball_2 = board.add_ball(r=10, x=520, y=500, vx=0, vy=0)

	ball_4 = board.add_ball(r=10, x = 500, y=520, vx = 0, vy=0)
	ball_3 = board.add_ball(r=10, x = 521, y=520, vx=0,vy=0)

	ball_5 = board.add_ball(r=10, x=510, y=430, vx=0, vy=1)	

def disp_balls(board):
	balls = board.get_balls_pygame()
	for ball in balls:
		center = (int(ball['x']), int(ball['y']))
		radius = int(ball['r'])
		pygame.draw.circle(screen, color, center, radius)

def disp_lenne(board):
	balls = board.get_balls_pygame()
	for ball in balls:
		center = (int(ball['x']), int(ball['y']))
		radius = int(ball['r'])
		screen.blit(lenne, center)

def start():
	while True:
		time.sleep(0.001)
		board.step()

add_balls10(board)
running = True
t = Thread(target = start)
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			try:
				t.start()
			except ValueError as e:
				print("Got Error of type "+ str(type(e)) +" and message "+e.message)
		if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
			board.step()

	screen.fill((0,0,0))
	disp_lenne(board)
	pygame.display.flip()

