# MIV 2018-2023

import numpy as np
import pygame

width = 600
height = 500

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

magenta = (212, 64, 219)
hunter_green = (8, 207, 124)
dark_grey = (28, 28, 28)
off_white = (237, 237, 237)

fps = 60
clock = pygame.time.Clock()

g = 9.8

m1 = 1
m2 = 1

# to scale the circle for better visualization (10 for kg, 100 for gr...)
m1_scale = 10
m2_scale = 10
radius1 = m1 * m1_scale
radius2 = m2 * m2_scale

r1 = 1
r2 = 1

# scale r for better visualization (100 for m, 1000 for cm...)
r1_scale = 100
r2_scale = 100

angle1 = np.pi / 2
angle2 = 3 * np.pi / 2

x1 = 0
y1 = 0
x2 = 0
y2 = 0

angle1_v = 0
angle2_v = 0

angle1_a = 0
angle2_a = 0

# the simulation will depend on the fps
delta_t = 1 / fps

pivotx = width / 2
pivoty = 150

# TODO add trail for first circle too
trail = []
trail_top = []
trail_length = 60

fontsize = 21

canvas = pygame.display.set_mode((width, height))

pygame.init()

endSim = False


def printOnScreen(msg, color, size, xcoord, ycoord):
    font = pygame.font.SysFont(None, size)
    text = font.render(msg, True, color)
    canvas.blit(text, [xcoord, ycoord])

# TODO draw lines between each circle
def draw_trail(list, color):
    for coord in list:
        pygame.draw.circle(canvas, color, (int(coord[0]), int(coord[1])), 1)

while not endSim:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            endSim = True

    canvas.fill(dark_grey)

    x1 = r1 * np.sin(angle1)
    y1 = r1 * np.cos(angle1)

    x2 = x1 + r2 * np.sin(angle2)
    y2 = y1 + r2 * np.cos(angle2)

    curr_pos = []
    curr_pos.append(pivotx + x2 * r2_scale)
    curr_pos.append(pivoty + y2 * r2_scale)

    if len(trail) >= trail_length:
        trail.remove(trail[0])
    
    if len(trail_top) >= trail_length:
        trail_top.remove(trail_top[0])

    trail.append(curr_pos)
    trail_top.append([pivotx + x1 * r1_scale, pivoty + y1 * r1_scale])

    # draw the trail
    draw_trail(trail, magenta)
    draw_trail(trail_top, hunter_green)

    pygame.draw.line(canvas, off_white, (int(pivotx), int(pivoty)),
                     (int(pivotx + x1 * r1_scale), int(pivoty + y1 * r1_scale)))
    pygame.draw.circle(canvas, off_white, (int(pivotx + x1 * r1_scale), 
                                           int(pivoty + y1 * r1_scale)), radius1)

    pygame.draw.line(canvas, off_white, (int(pivotx + x1 * r1_scale), int(pivoty + y1 * r1_scale)),
                     (int(pivotx + x2 * r2_scale), int(pivoty + y2 * r2_scale)))
    pygame.draw.circle(canvas, off_white, (int(pivotx + x2 * r2_scale), 
                                           int(pivoty + y2 * r2_scale)), radius2)

    # calculate the accelerations
    num1 = - g * (2 * m1 + m2) * np.sin(angle1)  # -
    num2 = m2 * g * np.sin(angle1 - 2 * angle2)  # -
    num3 = 2 * np.sin(angle1 - angle2)  # *
    num4 = m2 * (angle2_v ** 2 * r2 + angle1_v ** 2 * r1 * np.cos(angle1 - angle2))
    den = r1 * (2 * m1 + m2 - m2 * np.cos(2 * angle1 - 2 * angle2))

    angle1_a = (num1 - num2 - num3 * num4) / den

    num1 = 2 * np.sin(angle1 - angle2)  # * (
    num2 = angle1_v ** 2 * r1 * (m1 + m2)  # +
    num3 = g * (m1 + m2) * np.cos(angle1)  # +
    num4 = angle2_v ** 2 * r2 * m2 * np.cos(angle1 - angle2)
    den = r2 * (2 * m1 + m2 - m2 * np.cos(2 * angle1 - 2 * angle2))

    angle2_a = (num1 * (num2 + num3 + num4)) / den

    # calculate velocities and angles
    angle1_v = angle1_v + (delta_t * angle1_a)
    angle2_v = angle2_v + (delta_t * angle2_a)
    angle1 = angle1 + (delta_t * angle1_v)
    angle2 = angle2 + (delta_t * angle2_v)

    pE = - ((m1 + m2) * g * r1 * np.cos(angle1)) - (m2 * g * r2 * np.cos(angle2))
    kE = ((1 / 2) * m1 * r1 ** 2 * angle1_v ** 2) + ((1 / 2) * m2 *
         ((r1 ** 2 * angle1_v ** 2) + (r2 ** 2 * angle2_v ** 2) +
         (2 * r1 * r2 * angle1_v * angle2_v * np.cos(angle1 - angle2))))

    Et = pE + kE
    lagrangian = kE - pE

    # TODO rn this is calculated every frame, maybe change that?
    printOnScreen("Potential Energy (V) = {0:.2f} J".format(pE), off_white, fontsize, 0, 0)
    printOnScreen("Kinetic Energy (T) = {0:.2f} J".format(kE), off_white, fontsize, 0, fontsize)
    printOnScreen("Total Energy (Et) = {0:.2f} J".format(Et), off_white, fontsize, 0, fontsize * 2)
    printOnScreen("Lagrangian (L) = {0:.2f} Jp"
                  "".format(lagrangian), off_white, fontsize, 0, fontsize * 3)

    pygame.display.update()
    clock.tick(fps)
