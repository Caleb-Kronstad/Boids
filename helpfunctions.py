#imports
import pygame as py
from pygame import Vector2 as Vec2
import math
import random

#Some functions I created

def Normalize(vector): #using my own rather than np.linalg.norm gives a 30 fps boost alone -- crazy
    return math.sqrt(vector[0]**2 + vector[1]**2)

def LimitMagnitude(vector, limit):
    magnitude = Normalize(vector)
    if magnitude > limit:
        normalized_vector = vector / magnitude
        limited_vector = normalized_vector * limit
        return limited_vector
    else:
        return vector
    
def Clamp(num, min=0, max=1):
    if num < min:
        return min
    if num > max:
        return max
    return num
    
def SetMagnitude(vector, magnitude):
    if (Normalize(vector) > 0):
        normalized_vector = vector / Normalize(vector)
    else:
        return Vec2(0,0)
    scaled_vector = normalized_vector * magnitude
    return scaled_vector

def FindBoidSection(boid):
    xs = 0
    ys = 0
    
    if boid.pos.x > 1200:
        xs = 3
    elif boid.pos.x > 800:
        xs = 2
    elif boid.pos.x > 400:
        xs = 1

    if boid.pos.y > 600:
        ys = 2
    elif boid.pos.y > 300:
        ys = 1
    
    return [xs,ys]

def GenerateSpawnPointOffMap():
    randpos = random.randint(0,3)
    if randpos == 0: #top
        randx = random.randint(-50, 1650)
        randy = random.randint(-150, -50)
    elif randpos == 1: #bottom
        randx = random.randint(-50, 1650)
        randy = random.randint(950, 1100)
    elif randpos == 2: #left
        randx = random.randint(-150, -50)
        randy = random.randint(-50, 950)
    elif randpos == 3: #right
        randx = random.randint(1650, 1800)
        randy = random.randint(-50, 950)

    return randx, randy