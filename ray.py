
import pygame as py
import numpy as np
from colors import *

class Ray:
    def __init__(this, startPos, endPos, distance):
        this.startPos = startPos
        this.endPos = endPos
        this.distance = distance

def CastRay(startPos, endPos):
    dist = np.sqrt((endPos[0]-startPos[0])**2 + (endPos[1]-startPos[1])**2)
    ray = Ray(startPos, endPos, dist)
    return ray

def DrawRay(window, startPos, endPos, color=RED, width=1):
    py.draw.line(window, color, startPos, endPos, width)