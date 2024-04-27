#imports
import pygame as py
from pygame import Vector2 as Vec2
import math

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