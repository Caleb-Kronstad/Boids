
import pygame as py
from pygame import Vector2 as Vec2
import numpy as np
from colors import *

class Wall:
    def __init__(this, x1, y1, x2, y2):
        this.x1 = x1
        this.y1 = y1
        this.x2 = x2
        this.y2 = y2

    def DebugDraw(this, window, color=RED, width=3):
        py.draw.line(window, color, 
                     (this.x1, this.y1), 
                     (this.x2, this.y2),
                     width)

# only for drawing the ray onto the screen, not for calculating anything
class Ray:
    def __init__(this, pos, direction, distance):
        this.pos = pos
        this.direction = direction
        this.distance = distance

    def ChangeDirection(this, angle):
        this.direction = Vec2(np.cos(angle), np.sin(angle))
        
    def CastToWalls(this, walls):
        for wall in walls:
            intersectionPoint = GetLineIntersection(Vec2(wall.x1, wall.y1), Vec2(wall.x2, wall.y2),
                                                  Vec2(this.pos.x, this.pos.y), Vec2(this.direction.x * this.distance + this.pos.x, this.direction.y * this.distance + this.pos.y))
            if (intersectionPoint):
                return True
        return False

    def DebugDraw(this, window, color=RED, width=3):
        py.draw.line(window, color,
                     (this.pos.x, this.pos.y), 
                     (this.direction.x * this.distance + this.pos.x, this.direction.y * this.distance + this.pos.y),
                     width)

# Fast method for getting line intersections :D
# Gavin. “How Do You Detect Where Two Line Segments Intersect?” Stack Overflow, 28 Dec. 2009, stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect. 
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