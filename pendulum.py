# MIV 2018-2023

# http://www.maths.surrey.ac.uk/explore/michaelspages/documentation/Simple
# http://hyperphysics.phy-astr.gsu.edu/hbase/pendl.html#c2
# https://www.grc.nasa.gov/www/k-12/airplane/dragsphere.html
# https://en.wikipedia.org/wiki/Density_of_air

import numpy as np
import pygame

# colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 255, 0)
green = (0, 0, 255)

fontsize = 22

# window sizes
width = 600
height = 400

# position  coordinates of the pivot
pivotx = width / 2
pivoty = height / 4

fps = 60
clock = pygame.time.Clock()

endSim = False

g = 9.81  # m/s^2

# the mass, in kg
m = 1
mass_scale = 10  # to scale the circle for better visualization (10 for kg, 100 for gr...)
radius = m * mass_scale  # radius of the sphere

"""
# air drag (D = Cd * .5 * rho * V^2 * A)
drag = 0
cd = 0.47  # drag coefficient of a sphere
rho = 1.2754  # At IUPAC standard temperature and pressure (0 °C and 100 kPa), dry air has a density of 1.2754 kg/m^3
mass_area = 4 * np.pi * radius ** 2  # area of the spheric mass
"""

# position coordinates of the mass
x = 0
y = 0

# theta in rad
angle = np.pi / 2

# velocity (dtheta/dt) in m/s
angle_v = 0

# acceleration (d^2theta/dt^2) in m/s^2
angle_a = 0

# string length in m
r = 1
scale = 100  # scale r for better visualization (100 for m, 1000 for cm...)

# change in time
delta_t = 1 / fps

# data to display
period = (2 * np.pi * np.sqrt(r / g) * (1 + ((1/16) * angle ** 2) + ((11 / 3072) * angle ** 4)))  # s
total_force = 0  # N
angular_velocity = 0
linear_velocity = 0

pygame.init()

canvas = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simple pendulum simulation")


def printOnScreen(msg, color, size, xcoord, ycoord):
    font = pygame.font.SysFont(None, size)
    text = font.render(msg, True, color)
    canvas.blit(text, [xcoord, ycoord])


while not endSim:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            endSim = True

    canvas.fill(white)

    x = r * np.sin(angle)
    y = r * np.cos(angle)

    pygame.draw.line(canvas, black, (pivotx, pivoty), (pivotx + x * scale, pivoty + y * scale), 1)
    pygame.draw.circle(canvas, black, (int(pivotx + x * scale), int(pivoty + y * scale)), int(radius))

    angle_a = - (g / r) * np.sin(angle)
    angle_v = angle_v + (delta_t * angle_a)

    angle = angle + (delta_t * angle_v)

    # drag = cd * .5 * rho * linear_velocity ** 2 * mass_area
    # very simple dampening
    angle_v *= 0.999

    total_force = - m * g * np.sin(angle)
    angular_velocity = - (g / r) * np.sin(angle)
    linear_velocity = r * angular_velocity

    printOnScreen("Period (T) = {} s".format(period), black, fontsize, 0, 0)
    printOnScreen("Total force = {} N".format(total_force), black, fontsize, 0, fontsize)
    printOnScreen("Angular velocity = {} rad/s".format(angular_velocity), black, fontsize, 0, fontsize * 2)
    printOnScreen("Linear velocity = {} m/s".format(linear_velocity), black, fontsize, 0, fontsize * 3)
    # printOnScreen("Air drag = {}".format(drag), black, 0, 100)

    pygame.display.update()
    clock.tick(fps)
