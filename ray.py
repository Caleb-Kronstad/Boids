
import pygame as py
import numpy as np
from colors import *

class Ray:
    def __init__(this, position, direction, distance):
        this.position = position
        this.direction = direction
        this.distance = distance
        this.size = this.distance * this.direction
        this.rect = py.Rect(this.position[0], this.position[1], this.size[0], this.size[1])

    def Cast(this, position, direction):
        this.direction = direction
        this.position = position + (this.direction)
        this.size = this.distance * this.direction
        this.rect = py.Rect(this.position[0], this.position[1], this.size[0], this.size[1])

    def Draw(this, window, color=RED, width=1):
        py.draw.line(window, color, this.position, this.position + (this.distance * this.direction), width)