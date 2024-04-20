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
if (FULLSCREEN):
    window = py.display.set_mode((0,0), py.FULLSCREEN)
else:
    window = py.display.set_mode((screen_width, screen_height))

running = True
clock = py.time.Clock()
FPS = 60

boid_img = py.image.load('resources/circle_15px.png')

square_img = py.Surface((15,15), py.SRCALPHA)
square_img.fill(CYAN)

main_flock = []
for i in range(50):
    pos = Vec2(random.randint(0,screen_width), random.randint(0,screen_height))
    size = Vec2(square_img.get_size())
    angle = random.uniform(-np.pi,np.pi)
    speed = Vec2(5,5)
    ray1 = Ray(pos, angle, 0, 100)
    ray2 = Ray(pos, angle, np.pi/4, 100)
    ray3 = Ray(pos, angle, -np.pi/4, 100)
    rays = [ray1, ray2, ray3]
    
    boid = Boid_Old(pos, size, angle, speed, boid_img, rays)
    main_flock.append(boid)
    

flock = []
for i in range(50):
    pos = Vec2(screen_width/2, screen_height/2)
    vel = Vec2(random.uniform(-1,1), random.uniform(-1,1))
    accel = Vec2(0,0)
    
    boid = Boid(pos, vel, accel, boid_img)
    flock.append(boid)

while running:
    for e in py.event.get():
        if e.type == py.QUIT: running = False

    window.fill(DARKGRAY)

    for boid in flock:

        #SteeringForce = BoidSteeringForce(boid, main_flock, 50, 500, 300, 35, 10, 1)
        #NetForce = SteeringForce

        #boid.ApplyPhysics(NetForce)
        #boid.UpdateRotation(np.degrees(boid.expectedAngle))
        
        boid.Update()
        boid.Draw(window)

    py.display.flip()
    clock.tick(FPS)

py.quit()
