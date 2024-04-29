#imports
import pygame as py
from pygame import Vector2 as Vec2
from colors import *

class Door:
    def __init__(this, x, y, w, h, boids_needed):
        this.x = x
        this.y = y
        this.w = w
        this.h = h
        this.width = this.w
        this.height = this.h
        this.boids_needed = boids_needed
        this.open = False

        this.rect = py.Rect(x/2, y/2, w/2, h/2)

    def TryOpen(this, flock):
        if flock.num_boids >= this.boids_needed:
            this.open = True
            return True
        return False

    def Draw(this, window, color=PINK):
        if this.open: return

        if this.rect.x + this.rect.w >= 0 and this.rect.y + this.rect.h >= 0:
            py.draw.rect(window, PINK, this.rect, 5)