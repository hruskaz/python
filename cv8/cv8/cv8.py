from pygame import display, draw, time, event
import random
import pygame
import sys

screen = display.set_mode([800,600])
clock = time.Clock()
circles = []
random.seed()

while True:
	screen.fill([0,0,0])
	action = event.poll()
	if action.type == pygame.KEYDOWN:
		sys.exit()
	for i in range(len(circles)-1):
		lst = list(circles[i])
		lst[3] += 1
		circles[i] = tuple(lst)
		draw.circle(circles[i][0],circles[i][1],circles[i][2],circles[i][3],circles[i][4])
	
	reusedCircles = []
	for i in range(len(circles)):
		if circles[i][3] <= 80:
			reusedCircles.append(circles[i])
	circles = reusedCircles
	
	if len(circles) <= 20:
		circles.append((screen, [255,255,255], [random.randint(0,800),random.randint(0,600)],0,1))	
	display.flip()
	clock.tick(60)