
import pygame as py
from pygame import Vector2 as Vec2
import numpy as np
from colors import *

class Ray:
    def __init__(this, pos, angle, distance):
        this.pos = pos
        this.distance = distance
        this.angle = angle

        this.direction = Vec2(np.cos(angle), np.sin(angle))

    def Draw(this, window, width=1):
        py.draw.line(window, RED, 
                     (this.pos.x, this.pos.y), 
                     (this.direction.x * this.distance + this.pos.x, this.direction.y * this.distance + this.pos.y),
                     width)
        
    def Cast(this, other):
        x1 = other.pos.x
        y1 = other.pos.y
        x2 = other.pos.x + other.size.x
        y2 = other.pos.y + other.size.y
        x3 = this.pos.x
        y3 = this.pos.y
        x4 = this.pos.x + this.direction.x
        y4 = this.pos.y + this.direction.y

        den = (x1-x2) * (y3-y4) - (y1-y2) * (x3-x4)
        if den == 0:
            return
        
        t = ((x1-x3) * (y3-y4) - (y1-y3) * (x3-x4)) / den
        u = -((x1-x2) * (y1-y3) - (y1-y2) * (x1-x3)) / den
        if t > 0 and t < 1 and u > 0:
            pt = Vec2(0,0)
            pt.x = x1+t*(x2-x1)
            pt.y = y1+t*(y2-y1)
            return pt
        return