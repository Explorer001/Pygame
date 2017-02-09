import pygame
import random
import time

pygame.init()
windowSize = (1000, 720)
screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption('Life')
clock = pygame.time.Clock()

cellSize = 10

base03 = (0, 43, 54)
base00 = (101, 123, 131)
green = (133, 153, 0)
red = (220, 50, 47)

board = []
dx = 0
dy = 0

def buildBoard():
	global dx, dy, cellSize
	wx, wy = windowSize
	dx = wx/cellSize
	dy = wy/cellSize
	for i in range(0,dy):
		ylist = []
		for j in range(0,dx):
			ylist.append(0)
		board.append(ylist)

def drawRaster():
	global dx, dy, cellSize
	for x in range(0, dx*cellSize, cellSize):
		pygame.draw.line(screen, base00, (x,0), (x,dy*cellSize))	
	for y in range(0, dy*cellSize, cellSize):
		pygame.draw.line(screen, base00, (0,y), (dx*cellSize,y))

def printBoard():
	global board, cellSize
	screen.fill(base03)
	for y in range(len(board)):
		for x in range(len(board[y])):
			color = base03
			if board[y][x] == 1:
				color = green
			cell = pygame.Rect((x*cellSize, y*cellSize), (cellSize, cellSize))
			pygame.draw.rect(screen, color, cell, 0)
	drawRaster()

def getNextGen():
	global dx, dy, board
	tng = []
	for y in range(0,dy):
		for x in range(0,dx):
			cellStatus = board[y][x]
			newStatus = 0
			livAdjCount = getLivingAdjacentCount(x, y)
			if cellStatus == 0 and livAdjCount == 3:
				newStatus = 1
			elif cellStatus == 1:
				if livAdjCount < 2:
					newStatus = 0
				elif 2 <= livAdjCount <= 3:
					newStatus = 1
				elif livAdjCount > 3: 
					newStatus = 0
			tng.append((x,y,newStatus))
	for t in tng:
		nx,ny,st = t
		board[ny][nx] = st

def getLivingAdjacentCount(x, y):
	global dx, dy, board
	possible = [(x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y),(x+1,y),(x-1,y+1),(x,y+1),(x+1,y+1)]
	lifeCount = 0
	for p in possible:
		px,py = p
		if 0 <= px < dx and 0 <= py < dy:
			if board[py][px] == 1:
				lifeCount += 1	
	return lifeCount

def drawStructure(name, pos):
	global board, dx, dy
	points = []
	x,y = pos
	if name == 'blinker':
		points = [(x-1,y), (x,y),(x+1,y)]
	elif name == 'explosion':
		points = [(x-1,y-1),(x-1,y-2),(x-1,y-3),(x,y-3),(x+1,y-3),(x+1,y-2),(x+1,y-1),(x-1,y+1),(x-1,y+2),(x-1,y+3),(x,y+3),(x+1,y+3),(x+1,y+2),(x+1,y+1)]	
	elif name == 'pulsator':
		points = [(x-4,y),(x-3,y),(x-2,y-1),(x-2,y+1),(x-1,y),(x,y),(x+1,y),(x+2,y),(x+3,y-1),(x+3,y+1),(x+4,y),(x+5,y)]
	elif name == 'rPentomino':
		points = [(x,y),(x,y-1),(x,y+1),(x-1,y),(x+1,y-1)]
	elif name == 'random':
		for fy in range(0,dy):
			for fx in range(0,dx):
				rtd = random.randint(1,10)
				if rtd <= 6:
					points.append((fx,fy))	
	for p in points:
		tx,ty = p
		board[ty][tx] = 1

def editorMode():
	global board, cellSize
	while True:
		pygame.event.get()
		btn = pygame.mouse.get_pressed()
		a,b,c = btn
		if a == 1:
			x,y = pygame.mouse.get_pos()
			cx = x/cellSize
			cy = y/cellSize
			board[cy][cx] = (board[cy][cx]+1)%2
			time.sleep(0.5)
		elif c == 1:
			return
		printBoard()
		pygame.display.update()
		clock.tick(15)

def main():
	global board
	buildBoard()
	printBoard()
	editorMode()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_e:
					editorMode()
		printBoard()
		getNextGen()
		pygame.display.update()
		clock.tick(15)

main()
