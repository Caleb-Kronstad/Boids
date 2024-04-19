#import libraries to be used
import pygame as py
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

boids_list = []
for i in range(5):
    boidPosition = np.array([random.randint(0,screen_width),random.randint(0,screen_height)])
    boidSpeed = np.array([3, 3])
    boidSize = np.array([15,15])
    boidRange = 50 #boid's view range, how far it can see in front of itself

    boidDirection = np.array([random.uniform(-1,1),random.uniform(-1,1)])
    boidDirectionNorm = np.linalg.norm(boidDirection)
    boidDirectionHat = boidDirection / boidDirectionNorm

    boidRay = Ray(boidPosition, boidDirection, 50) #ray position, direction, distance

    boid = Boid(boid_img, boidPosition, boidSize, boidDirectionHat, boidSpeed, boidRange, boidRay)
    boids_list.append(boid)

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
    for boid in boids_list:
            
        close_boids = []
        for boid_2 in boids_list:
            dist = np.sqrt((boid_2.position[0] - boid.position[0])**2 + (boid_2.position[1] - boid.position[1])**2)
            if (dist < boid.viewRange):
                close_boids.append(boid_2)
                #py.draw.line(window, RED, boid.position, boid_2.position, 1) ## only for debugging -- draws a line between boids that are near eachother

        repulsiveForce = np.array([0,0])
        for boid_near in close_boids:
            dir = boid.direction + RepulsiveForce(boid.position, boid_near.position) / len(close_boids)
            dirNorm = np.linalg.norm(dir)
            dirHat = dir / dirNorm

            repulsiveForce = repulsiveForce + dirHat

        repulsiveForceNorm = np.linalg.norm(repulsiveForce)
        repulsiveForceHat = repulsiveForce / repulsiveForceNorm
        
        boid.direction = repulsiveForceHat

        boid.Move()
        boid.ray.Cast(boid.position + boid.size/2, boid.direction)
        #boid.ray.Draw(window, width=5)
        boid.Draw(window)

    py.display.flip()
    clock.tick(FPS)

py.quit()