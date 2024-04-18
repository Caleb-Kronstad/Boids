#import libraries to be used
import pygame as py
import numpy as np
import random

#import other files
from colors import *
from bird import *
from ray import *

py.init()
screen_width, screen_height = 1600, 900
window = py.display.set_mode((screen_width, screen_height))
py.display.set_caption("Boids")

running = True
clock = py.time.Clock()
FPS = 60

bird_img = py.image.load('resources/bird.png')

birds_list = []
for i in range(0,10):
    randomPosition = np.array([random.randint(0,screen_width),random.randint(0,screen_height)])
    birdSpeed = np.array([5, 5])
    birdSize = np.array([25,25])
    birdVR = 25 #bird's view range, how far it can see in front of itself

    # old way of calculating a random direction vector, now im using trig cause it's a lot simpler
    #randomDirection = np.array([random.uniform(-1,1),random.uniform(-1,1)])
    #randomDirectionNorm = np.linalg.norm(randomDirection)
    #normalizedRandomDirection = randomDirection / randomDirectionNorm

    randomAngle = random.randint(0,360)

    bird = Bird(bird_img, randomPosition, birdSize, CYAN, birdSpeed, randomAngle, birdVR)
    birds_list.append(bird)

while running:
    for e in py.event.get():
        if e.type == py.QUIT: running = False

    window.fill(DARKGRAY)
    for i in range(0,len(birds_list)):
        birds_list[i].Move()
        birds_list[i].Update(window)
        
        #for j in range(0, 4):
        #    newPos = birds_list[i].position + (birds_list[i].size/2)
        #    newDir = birds_list[i].direction * directions[j] * 50
        #    ray = CastRay(newPos, newPos + newDir)
        #    DrawRay(window, ray.startPos, ray.endPos, width=5)

    py.display.flip()
    clock.tick(FPS)

py.quit()