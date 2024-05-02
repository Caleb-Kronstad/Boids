#imports
import pygame as py
from pygame import Vector2 as Vec2
from helpfunctions import *
import numpy as np

class Enemy:
    def __init__(this, pos, vel,  accel, img, max_speed=4, max_force=0.2, mass=1):
        this.pos = pos
        this.vel = vel
        this.accel = accel
        
        this.img = img
        this.saved_img = img

        this.max_speed = max_speed
        this.max_force = max_force

        this.forces = accel * mass

    def Update(this):
        this.accel = this.forces / this.mass
        this.vel = LimitMagnitude(this.vel + this.accel, this.max_speed)
        this.pos += this.vel
        this.forces = Vec2(0,0) # reset forces for next frame

        this.img = py.transform.rotate(this.saved_img, (180/np.pi) * (np.arctan2(-this.vel.y, this.vel.x) - (90 * (np.pi/180))))