
import pygame as py
from pygame import Vector2 as Vec2
import numpy as np
from colors import *

class Ray:
    def __init__(this, pos, direction, distance):
        this.pos = pos
        this.distance = distance
        this.direction = direction

    def LookAt(this, x, y):
        this.direction.x = x - this.pos.x
        this.direction.y = y - this.pos.y

        try:
            div = (this.direction and this.direction.normalize())
            this.direction.x /= div.x
            this.direction.y /= div.y
        except ZeroDivisionError:
            this.direction.x = 1
            this.direction.y = 0

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