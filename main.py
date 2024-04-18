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

birds_list = []
for i in range(0,1):
    randomPosition = np.array([random.randint(0,screen_width),random.randint(0,screen_height)])
    birdSpeed = np.array([5, 5])
    birdSize = np.array([25,25])
    birdVR = 25 #bird's view range, how far it can see in front of itself

    randomDirection = np.array([random.uniform(-1,1),random.uniform(-1,1)])
    randomDirectionNorm = np.linalg.norm(randomDirection)
    normalizedRandomDirection = randomDirection / randomDirectionNorm

    bird = Bird(randomPosition, birdSize, CYAN, birdSpeed, normalizedRandomDirection, birdVR)
    birds_list.append(bird)

while running:
    for e in py.event.get():
        if e.type == py.QUIT: running = False

    window.fill(DARKGRAY)
    for i in range(0,len(birds_list)):
        birds_list[i].StepPosition()

        directions = [np.array([0,1]), np.array([1,0]), np.array([0,0]), np.array([1,1])]
        for j in range(0, 4):
            newPos = birds_list[i].position + (birds_list[i].size/2)
            newDir = birds_list[i].direction * directions[j] * 50
            ray = CastRay(newPos, newPos + newDir)
            DrawRay(window, ray.startPos, ray.endPos, width=5)

        birds_list[i].Update(window)

    py.display.flip()
    clock.tick(FPS)

py.quit()