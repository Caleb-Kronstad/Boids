#imports
import pygame as py
from pygame import Vector2 as Vec2
import numpy as np
import random, sys

from boid import *
from helpfunctions import *

class Flock:
    def __init__(this, boids, pos, vel, max_speed, range, img, mass=1):
        this.boids = boids
        this.pos = pos
        this.vel = LimitMagnitude(vel, max_speed)
        this.max_speed = max_speed
        this.range = range
        this.mass = mass

        this.num_boids = 0

        this.forces = Vec2(0,0)

        this.angle = np.degrees(np.arctan2(-this.vel.y, this.vel.x) - np.radians(90))

        this.img = img
        this.saved_img = img

        this.furthest_boid = this.FindFurthestBoidFromFlockCenter()

    def FindFurthestBoidFromFlockCenter(this):
        furthest_boid = None
        furthest_distance = 0
        for boid in this.boids.values():
            dist_from_center = Normalize(boid.pos - this.pos)
            if dist_from_center > furthest_distance:
                furthest_distance = dist_from_center
                furthest_boid = boid

        return furthest_boid
    
    def AddFlockCenterForce(this, force=Vec2(0,0)):
        this.forces += force

    def UpdatePosition(this, velocity):
        new_pos = this.pos

        if new_pos.x > 1425:
            new_pos.x = 1425
        elif new_pos.x < 175:
            new_pos.x = 175
        if new_pos.y > 800:
            new_pos.y = 800
        elif new_pos.y < 100:
            new_pos.y = 100
        
        new_pos += velocity

        return new_pos

    def Update(this):
        if this.forces != Vec2(0,0):
            this.angle = np.degrees(np.arctan2(-this.vel.y, this.vel.x) - np.radians(90))
        accel = this.forces / this.mass
        this.vel = LimitMagnitude(this.vel + accel, this.max_speed)
        this.pos = this.UpdatePosition(this.vel)
        this.forces = Vec2(0,0)

        #this.furthest_boid = this.FindFurthestBoidFromFlockCenter()
        this.img = py.transform.rotate(this.saved_img, this.angle)

    def Draw(this, window):
        this.rect = this.img.get_rect(center = this.pos)
        drawn_rect = window.blit(this.img, this.rect)
        return drawn_rect