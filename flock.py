#imports
import pygame as py
from pygame import Vector2 as Vec2
import numpy as np
import random, sys

from boid import *
from helpfunctions import *
from ray import *

class Flock:
    def __init__(this, pos, vel, max_speed, range, img, mass=1):
        this.boids = {}
        this.pos = pos
        this.vel = LimitMagnitude(vel, max_speed)
        this.max_speed = max_speed
        this.saved_max_speed = max_speed
        this.range = range
        this.mass = mass

        this.last_vel = vel

        this.collision_type = None
        this.has_collision = False
        this.num_boids = 0

        this.stunned = False
        this.stun_timer = 30
        this.stun_length = this.stun_timer

        this.forces = Vec2(0,0)
        this.angle = np.degrees(np.arctan2(-this.vel.y, this.vel.x) - np.radians(90))

        this.img = img
        this.saved_img = img

        this.rect = this.img.get_rect(center = this.pos)
    
    def AddFlockCenterForce(this, force=Vec2(0,0)):
        this.forces += force
    
    def Movement(this, movement_vector):
        if movement_vector == Vec2(0,0): # check for no input
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
        if collide_index != -1 and this.stunned == False:
            wall = wall_rects[collide_index]
            this.forces = Vec2(0,0)
            this.vel = (-this.last_vel) * 4

            this.has_collision = True
            this.stunned = True
            this.max_speed = 10
            return True
        
        this.max_speed = this.saved_max_speed
        this.collision_type = None
        this.has_collision = False
        return False

    def Update(this):
        if this.stunned:
            this.stun_timer -= 1
            if this.stun_timer <= 0:
                this.stunned = False
                this.stun_timer = this.stun_length
        
        if this.vel != Vec2(0,0):
            this.angle = np.degrees(np.arctan2(-this.vel.y, this.vel.x) - np.radians(90))
        accel = this.forces / this.mass
        this.vel = LimitMagnitude(this.vel + accel, this.max_speed)
        this.pos += this.vel
        this.last_vel = this.vel
            
        this.forces = Vec2(0,0)

        #this.furthest_boid = this.FindFurthestBoidFromFlockCenter()
        this.img = py.transform.rotate(this.saved_img, this.angle)

    def Draw(this, window):
        this.rect = this.img.get_rect(center = this.pos)
        temp_rect = window.blit(this.img, this.rect)
        return temp_rect