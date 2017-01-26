import pygame

pygame.init()
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Controller')
clock = pygame.time.Clock()

base03 = (0, 43, 54)
base02 = (7, 54, 66)
base01 = (88, 110, 117)
base00 = (101, 123, 131)
base0 = (131, 148, 150)
base1 = (147, 161, 161)
red = (220, 50, 47)
green = (133, 153, 0)

Upper = 5
Lower = 40
Left = 100
Right = 5
Space = 1
radius = 10
throttleMode = 1

def main():
	while True:
		run()
		pygame.quit()
		quit()

def run():
	pygame.joystick.init()
	controller = getControllers()
	if not controller:
		print 'Oops... No Controllers connected!'
		return
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
		axes = getAxes(controller[0])
		drawGUI()
		drawPointer(axes)
		pygame.display.update()
		clock.tick(60)

def drawPointer(axes):
	dx, dy = size
	mx = ((dx-Left-Right)/2)+Left
	my = ((dy-Upper-Lower)/2)+Upper
	xmax = ((dx-Left-Right)/2)-radius
	ymax = ((dy-Upper-Lower)/2)-radius
	xaxis = axes[0]
	yaxis = axes[1]
	throttleLeft = 0
	throttleRight = 0
	tilt = axes[3]
	pygame.draw.circle(screen, red, (mx+int(xmax*xaxis),my+int(ymax*yaxis)), radius, 0)
	timax = (dx-Left-Right)/2
	thmaxL = 0
	thmaxR = 0
	colorL = red
	colorR = red
	thrL = 0
	thlR = 0
	if throttleMode == 0:
		throttleLeft = axes[2]
        	throttleRight = axes[4]
		colorL = red if throttleLeft > 0 else green
        	colorR = red if throttleRight > 0 else green
		thmaxL = (dy-Upper-Lower)/2
                thmaxR = (dy-Upper-Lower)/2
		thrL = pygame.Rect((Space, my), ((Left/2)-2*Space, int(thmaxL*throttleLeft)+1))
		thrR = pygame.Rect(((Left/2)+Space, my), ((Left/2)-3*Space, int(thmaxL*throttleRight)+1))	
	else:
		throttleLeft = (-1*axes[2]+1)/2
        	throttleRight = (-1*axes[4]+1)/2
		thmaxL = (dy-Upper-Lower)
	        thmaxR = (dy-Upper-Lower)
		thrL = pygame.Rect((Space, dy-Lower), ((Left/2)-2*Space, -1*int(thmaxL*throttleLeft)+1))
		thrR = pygame.Rect(((Left/2)+Space, dy-Lower), ((Left/2)-3*Space, -1*int(thmaxR*throttleRight)+1))
	tilR = pygame.Rect((mx, dy-Lower+Space), (int(timax*tilt), dy-Space))
	pygame.draw.rect(screen, colorL, thrL, 0)
	pygame.draw.rect(screen, colorR, thrR, 0)
	pygame.draw.rect(screen, red, tilR, 0)

def drawGUI():
	dx, dy = size
	axisRect = pygame.Rect((Left, Upper), (dx-Right-Left, dy-Upper-Lower))
	throttle1 = pygame.Rect((Space, Upper),((Left/2)-2*Space, dy-Upper-Lower))
	throttle2 = pygame.Rect(((Left/2)+Space, Upper),((Left/2)-3*Space, dy-Upper-Lower))
	tilt = pygame.Rect((Left, dy-Lower+Space),(dx-Right-Left, Lower-2*Space))
	screen.fill(base03)
	pygame.draw.rect(screen, base02, axisRect, 0)
	pygame.draw.rect(screen, base00, axisRect, 1)
	pygame.draw.rect(screen, base02, throttle1, 0)
	pygame.draw.rect(screen, base00, throttle1, 1)
	pygame.draw.rect(screen, base02, throttle2, 0)
	pygame.draw.rect(screen, base00, throttle2, 1)
	pygame.draw.rect(screen, base02, tilt, 0)
	pygame.draw.rect(screen, base00, tilt, 1)
	pygame.draw.line(screen, base00, (Space, ((dy-Upper-Lower)/2)+Upper), ((Left/2)-2*Space, ((dy-Upper-Lower)/2)+Upper), 1)
	pygame.draw.line(screen, base00, ((Left/2)+2*Space, ((dy-Upper-Lower)/2)+Upper), (Left-Space-2, ((dy-Upper-Lower)/2)+Upper), 1)
	pygame.draw.line(screen, base00, (((dx-Left-Right)/2)+Left, dy-Lower+Space), (((dx-Left-Right)/2)+Left, dy-Space-1), 1)
	ylines = (((dx-Left-Right)/2)+Left, Upper)
	ylinee = (((dx-Left-Right)/2)+Left, dy-Lower-1)
	xlines = (Left,((dy-Upper-Lower)/2)+Upper)
	xlinee = (dx-Right-1, ((dy-Upper-Lower)/2)+Upper)
	pygame.draw.line(screen, base00, xlines, xlinee, 1)
	pygame.draw.line(screen, base00, ylines, ylinee, 1)

def getAxes(controller):
	re = []
	for i in range(0, controller.get_numaxes()):
		re.append(controller.get_axis(i))
	return re	

def getControllers():
	re = []
	for i in range(pygame.joystick.get_count()):
		pygame.joystick.Joystick(i).init()
		re.append(pygame.joystick.Joystick(i))
	return re	

main()

