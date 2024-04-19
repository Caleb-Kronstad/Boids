#imports
import pygame as py
from pygame import Vector2 as Vec2
import numpy as np
from colors import *
from ray import *

class Boid:
    def __init__(this, pos, vel, size, img, ray, accl=Vec2(0,0), mass=1.0):
        this.pos = pos
        this.vel = vel
        this.size = size
        this.accl = accl
        this.mass = mass
        
        this.ray = ray
        this.img = img
        this.savedImg = img

        this.rect = img.get_rect(center = this.pos)

    def ApplyPhysics(this, forces):
        this.accl = forces * this.mass
        this.vel = this.vel + this.accl
        this.pos = this.pos + this.vel

        #prevent boid from going off screen
        if (this.pos.x >= 1600):
            this.pos = Vec2(0, this.pos.y)
        elif (this.pos.x <= 0):
            this.pos = Vec2(1600, this.pos.y)
        if (this.pos.y >= 900):
            this.pos = Vec2(this.pos.x, 0)
        elif (this.pos.y <= 0):
            this.pos = Vec2(this.pos.x, 900)

    def Rotate(this, angle): #rotates in degrees
        angle = Vec2.angle_to(this.pos, this.pos + this.vel)
        this.img = py.transform.rotate(this.savedImg, angle)
        this.rect = this.img.get_rect(center = this.pos)

    def Draw(this, window):
        window.blit(this.img, this.rect)