#imports
import pygame as py
from pygame import Vector2 as Vec2
import numpy as np
from colors import *
from ray import *

class Boid:
    def __init__(this, pos, vel, accel, img, mass=1):
        this.pos = pos
        this.accel = accel
        this.mass = mass
        
        this.vel = vel / np.linalg.norm(vel)

        this.angle = np.arctan2(this.vel.y, this.vel.x)
        this.img = img
        this.savedImg = img

    def Align(this, flock):
        avg = Vec2(0,0)
        align_dist = 100
        num_align = 0
        
        for other in flock:
            if other == this: continue

            dist = np.linalg.norm(this.pos, other.pos)
            if dist < align_dist:
                avg += other.vel
                num_align += 1
        
        if num_align > 0:
            avg /= num_align

        this.vel = avg

    def Update(this, forces=Vec2(0,0)):
        this.accel = forces * this.mass
        this.vel += this.accel
        this.pos += this.vel

    def Draw(this, window):
        this.img = py.transform.rotate(this.savedImg, np.degrees(this.angle))
        this.rect = this.img.get_rect(center = this.pos)
        window.blit(this.img, this.rect)

class Boid_Old:
    def __init__(this, pos, size, angle, speed, img, rays, mass=1.0):
        this.pos = pos
        this.size = size
        this.speed = speed
        this.mass = mass
        this.angle = angle

        this.accel = Vec2(0,0)
        this.vel = Vec2(np.cos(angle), np.sin(angle))
        this.vel.x *= this.speed.x
        this.vel.y *= this.speed.y
        
        this.rays = rays
        this.img = img
        this.savedImg = img

        this.rect = img.get_rect(center = this.pos)

        this.expectedAngle = angle

    def ApplyPhysics(this, forces=Vec2(0,0)):
        this.vel = Vec2(np.cos(this.angle), np.sin(this.angle))
        this.vel.x *= this.speed.x
        this.vel.y *= this.speed.y

        this.accel = forces * this.mass
        this.vel = this.vel + this.accel
        this.pos = this.pos + this.vel

        this.expectedAngle = np.arctan2(this.vel.y, this.vel.x)
        if (this.expectedAngle - this.angle > 0.1):
            this.angle += np.radians(1)

        #prevent boid from going off screen
        if (this.pos.x >= 1600):
            this.pos = Vec2(0, this.pos.y)
        elif (this.pos.x + this.size.x <= 0):
            this.pos = Vec2(1600, this.pos.y)
        if (this.pos.y >= 900):
            this.pos = Vec2(this.pos.x, 0)
        elif (this.pos.y + this.size.y <= 0):
            this.pos = Vec2(this.pos.x, 900)

    def Rotate(this, angle):
        this.angle = angle

    def UpdateRotation(this, angle_degrees): #rotates in degrees
        this.img = py.transform.rotate(this.savedImg, angle_degrees)
        this.rect = this.img.get_rect(center = this.pos)

    def Draw(this, window):
        window.blit(this.img, this.rect)