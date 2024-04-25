#imports
import pygame as py
from pygame import Vector2 as Vec2
import numpy as np
import random, sys

from boid import *
from helpfunctions import *

class Flock:
    def __init__(this, pos, vel, max_speed, range, img, mass=1):
        this.boids = {}
        this.pos = pos
        this.vel = LimitMagnitude(vel, max_speed)
        this.max_speed = max_speed
        this.saved_max_speed = max_speed
        this.range = range
        this.mass = mass

        this.has_collision = False
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
    
    def Movement(this, movement_vector):
        if movement_vector == Vec2(0,0) and this.has_collision == False: # check for staying still
            if this.vel.y > 0:
                this.vel.y -= 0.1
                if this.vel.y < 0:
                    this.vel.y = 0
            elif this.vel.y < 0:
                this.vel.y += 0.1
                if this.vel.y > 0:
                    this.vel.y = 0

            if this.vel.x > 0:
                this.vel.x -= 0.1
                if this.vel.x < 0:
                    this.vel.x = 0
            elif this.vel.x < 0:
                this.vel.x += 0.1
                if this.vel.x > 0:
                    this.vel.x = 0
    
    def CheckCollisions(this, wall_rects):
        collide_index = this.rect.collidelist(wall_rects)
        if collide_index != -1:
            this.max_speed = 0
            this.has_collision = True
            return True
        this.max_speed = this.saved_max_speed
        this.has_collision = False
        return False

    def Update(this):
        if this.has_collision: return

        if this.vel != Vec2(0,0):
            this.angle = np.degrees(np.arctan2(-this.vel.y, this.vel.x) - np.radians(90))
        accel = this.forces / this.mass
        this.vel = LimitMagnitude(this.vel + accel, this.max_speed)
        this.pos += this.vel
            
        this.forces = Vec2(0,0)

        #this.furthest_boid = this.FindFurthestBoidFromFlockCenter()
        this.img = py.transform.rotate(this.saved_img, this.angle)

    def Draw(this, window):
        this.rect = this.img.get_rect(center = this.pos)
        drawn_rect = window.blit(this.img, this.rect)
        return drawn_rect