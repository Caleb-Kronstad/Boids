
import pygame as py
from pygame import Vector2 as Vec2
import numpy as np
from colors import *

# only for drawing the ray onto the screen, not for calculating anything
class SimpleRay:
    def __init__(this, pos, direction, distance):
        this.pos = pos
        this.direction = direction
        this.distance = distance

    def Draw(this, window, width=3, color=RED):
        py.draw.line(window, color,
                     (this.pos.x, this.pos.y), 
                     (this.direction.x * this.distance + this.pos.x, this.direction.y * this.distance + this.pos.y),
                     width)

class Ray:
    def __init__(this, pos, angle, angle_offset=0, distance=100):
        this.pos = pos
        this.angle_offset = angle_offset
        this.distance = distance
        this.direction = Vec2(np.cos(angle+angle_offset), np.sin(angle+angle_offset))

    def ChangeDirection(this, angle):
        angle += this.angle_offset
        this.direction = Vec2(np.cos(angle), np.sin(angle))

    def Draw(this, window, width=1):
        py.draw.line(window, RED, 
                     (this.pos.x, this.pos.y), 
                     (this.direction.x * this.distance + this.pos.x, this.direction.y * this.distance + this.pos.y),
                     width)
        
    def Cast(this, other):
        for ray in other.rays:
            intersectionPoint = GetLineIntersection(Vec2(ray.pos.x, ray.pos.y), Vec2(ray.direction.x * ray.distance + ray.pos.x, ray.direction.y * ray.distance + ray.pos.y),
                                                  Vec2(this.pos.x, this.pos.y), Vec2(this.direction.x * this.distance + this.pos.x, this.direction.y * this.distance + this.pos.y))
            if (intersectionPoint):
                return True
        return False

# Fast method for getting line intersections :D
# Gavin, 12/28/2009, stackoverflow.com. https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect 4/21/2024
def GetLineIntersection(p1, p2, p3, p4):
    s1 = Vec2(0,0)
    s1.x = p2.x - p1.x
    s1.y = p2.y - p1.y

    s2 = Vec2(0,0)
    s2.x = p4.x - p3.x
    s2.y = p4.y - p3.y

    s = (-s1.y * (p1.x - p3.x) + s1.x * (p1.y - p3.y)) / (-s2.x * s1.y + s1.x * s2.y)
    t = (s2.x * (p1.y - p3.y) - s2.y * (p1.x - p3.x)) / (-s2.x * s1.y + s1.x * s2.y)

    if (s >= 0 and s <= 1 and t >= 0 and t <= 1):
        return True # collision detected
    return False # no collision detected