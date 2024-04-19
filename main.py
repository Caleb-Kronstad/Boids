##--- TEMPORARY CITATIONS ---
# https://www.cs.trinity.edu/~jhowland/cs2322/2d/2d/
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

py.init()
screen_width, screen_height = 1600, 900
py.display.set_caption("Boids")
FULLSCREEN = False
if (FULLSCREEN):
    window = py.display.set_mode((0,0), py.FULLSCREEN)
else:
    window = py.display.set_mode((screen_width, screen_height))

running = True
clock = py.time.Clock()
FPS = 60

boid_img = py.image.load('resources/bird.png')
square_img = py.Surface((25,25), py.SRCALPHA)
square_img.fill(CYAN)

main_flock = []
for i in range(5):
    pos = Vec2(random.randint(0,screen_width), random.randint(0,screen_height))
    size = Vec2(square_img.get_size())
    
    velArr = np.array([random.uniform(-1,1), random.uniform(-1,1)])
    velNorm = np.linalg.norm(velArr)
    velHat = velArr / velNorm
    vel = Vec2(velHat[0], velHat[1])

    ray = Ray(pos, vel, 50)
    
    boid = Boid(pos, vel, size, square_img, ray)
    main_flock.append(boid)

def RepulsiveForce(pos1, pos2):
    r = pos2 - pos1
    rmag = np.linalg.norm(r)
    if (rmag == 0):
        return 0
    rhat = r/rmag
    F = (-1 * rhat)
    return F

while running:
    for e in py.event.get():
        if e.type == py.QUIT: running = False

    window.fill(DARKGRAY)
    
    for boid in main_flock:
        boid.ApplyPhysics(Vec2(0,0))
        boid.Rotate(0)
        boid.Draw(window)
        boid.ray.pos = boid.pos
        boid.ray.Draw(window, width=5)

    py.display.flip()
    clock.tick(FPS)

py.quit()