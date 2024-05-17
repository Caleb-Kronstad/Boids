
import pygame as py
from pygame import Vector2 as Vec2
from colors import *

class Ray: # simple ray class
    def __init__(this, pos, direction, distance): # initialize ray
        this.pos = pos
        this.direction = direction
        this.distance = distance

    def DebugDraw(this, window, color=RED, width=1): # draw ray
        py.draw.line(window, color,
                     (this.pos.x, this.pos.y), 
                     (this.direction.x * this.distance + this.pos.x, this.direction.y * this.distance + this.pos.y),
                     width)

# Fast method for getting line intersections :D
# Ended up not using, but will keep here cause I think it's valuable to have
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