# MIV 2018-2023

# TODO this is still a WIP, far from finished

import numpy as np
import pygame

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 255, 0)
green = (0, 0, 255)

width = 600
height = 600

g = 9.8
pivot1x = width/5
pivotY = height / 5
pivot2x = (width/4) * 2
x1 = 0
y1 = 0
x2 = 0
y2 = 0
angle1 = np.pi/4
angle2 = 0
angle1_v = 0
angle2_v = 0
angle1_a = 0
angle2_a = 0
m1 = 400
m2 = 400
r1 = 100
r2 = 100
k = 20

fps = 24
clock = pygame.time.Clock()

endSim = False

pygame.init()

canvas = pygame.display.set_mode((width, height))

while not endSim:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            endSim = True

    num1 = np.sin(angle1)  # *
    num2 = m1 * (r1 * (angle1_v * angle1_v) - g) - k * r1  # +
    num3 = k * r2 * np.sin(angle2)
    den = m1 * r1 * np.cos(angle1)

    angle1_a = (num1 * num2 + num3) / den

    num1 = np.sin(angle2)  # *
    num2 = m2 * (r2 * (angle2_v * angle2_v) - g) - k * r2  # +
    num3 = k * r1 * np.sin(angle1)
    den = m2 * r2 * np.cos(angle2)

    angle2_a = (num1 * num2 + num3) / den

    canvas.fill(white)

    x1 = r1 * np.sin(angle1)
    y1 = r1 * np.cos(angle1)

    x2 = r2 * np.sin(angle2)
    y2 = r2 * np.cos(angle2)

    pygame.draw.line(canvas, black, (pivot1x + r1, pivotY + r1), (int(pivot1x + r1 + x1), int(pivotY + r1 + y1)))
    pygame.draw.line(canvas, black, (pivot2x + r2, pivotY + r1), (int(pivot2x + r2 + x2), int(pivotY + r2 + y2)))

    pygame.draw.line(canvas, black, (int(pivot1x+r1+x1), int(pivotY + r1 + y1)), (int(pivot2x + r2 + x2), int(pivotY + r2 + y2)))

    pygame.draw.circle(canvas, black, (int(pivot1x+r1+x1), int(pivotY + r1 + y1)), 10, 0)
    pygame.draw.circle(canvas, black, (int(pivot2x+r2+x2), int(pivotY + r2 + y2)), 10, 10)

    angle1_v += angle1_a
    angle2_v += angle2_a
    
    angle1 += angle1_v
    angle2 += angle2_v

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()
