##--- TEMPORARY CITATIONS ---
# https://www.cs.trinity.edu/~jhowland/cs2322/2d/2d/
# https://stackoverflow.com/questions/6247153/angle-from-2d-unit-vector
# https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
# https://www.youtube.com/watch?v=HzR-9tfOJQo
##---

#import libraries to be used
import pygame as py
from pygame import Vector2 as Vec2
import numpy as np
import random

#import other files
from colors import *
from boid import *
from ray import *
from boid_rules import *

py.init()
screen_width, screen_height = 1600, 900
py.display.set_caption("Boids")
FULLSCREEN = False
window = py.display.set_mode((screen_width, screen_height))

running = True
clock = py.time.Clock()
FPS = 60

boid_img = py.image.load('resources/circle_15px.png')
arrow_img = py.image.load('resources/arrow.png')

sections = {
    0: { 0: {}, 1: {}, 2: {} },
    1: { 0: {}, 1: {}, 2: {} },
    2: { 0: {}, 1: {}, 2: {} },
    3: { 0: {}, 1: {}, 2: {} }
}

for i in range(100):
    pos = Vec2(random.randint(0,screen_width), random.randint(0,screen_height))
    vel = Vec2(random.uniform(-1,1), random.uniform(-1,1))
    accel = Vec2(1,1)
    
    boid = Boid(pos, vel, accel, boid_img)
    sections[boid.section[0]][boid.section[1]][(boid.id)] = boid

while running:
    for e in py.event.get():
        if e.type == py.QUIT: running = False

    window.fill(DARKGRAY)

    for x in sections.keys():
        for y in sections[x].keys():
            for boid in sections[x][y].values():
                boid.Flock(sections[x][y])
                boid.Update()
                sections = boid.UpdateSections(sections)
                boid.Draw(window)

    py.display.flip()
    clock.tick(FPS)

py.quit()
