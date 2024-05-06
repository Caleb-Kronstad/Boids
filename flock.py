#imports
import pygame as py
from pygame import Vector2 as Vec2
import numpy as np
import random, sys

from boid import *
from helpfunctions import *
from ray import *

class FlockParams():
    def __init__(this, separation_distance = 50, alignment_distance = 100, cohesion_distance = 200, separation_factor = 1, alignment_factor = 1, cohesion_factor = 1):
        this.separation_distance = separation_distance
        this.alignment_distance = alignment_distance
        this.cohesion_distance = cohesion_distance
        this.separation_factor = separation_factor
        this.alignment_factor = alignment_factor
        this.cohesion_factor = cohesion_factor

class Flock:

    ###--- INIT FUNCTION

    def __init__(this, pos, vel, speed, range, health, img, mass=1):
        # initialize member variables
        this.pos = pos
        this.speed = speed
        this.saved_speed = speed
        this.max_speed = 50
        this.vel = LimitMagnitude(vel, this.max_speed)
        this.range = range
        this.mass = mass

        this.coins = 0

        this.health = health

        this.boid_damage = 1

        this.num_boids = 0
        this.last_vel = vel

        this.collision_type = None
        this.has_collision = False
        this.num_boids = 0

        this.screen_pos = Vec2(800, 450)

        this.stunned = False
        this.stun_timer = 30
        this.stun_length = this.stun_timer

        this.forces = Vec2(0,0)
        this.angle = np.degrees(np.arctan2(-this.vel.y, this.vel.x) - np.radians(90))

        this.img = img
        this.saved_img = img

        this.rect = this.img.get_rect(center = this.screen_pos)
        this.CalculateCollisionRect()

        #Upgrades
        this.dashing = False
        this.dash_cooldown = 15
        this.dash_timer = this.dash_cooldown

        this.can_launch = True
        this.launch_cooldown = 15
        this.launch_timer = this.launch_cooldown
        
    ###---

    ###--- UPGRADES

    # Dash
    def Dash(this, force):
        if this.dashing: return # make sure not already dashing
        this.AddForce(force) # add dashing force
        this.speed = this.max_speed / 15 # change speed 
        this.dashing = True # dashing flag set to true
    def DashCooldown(this):
        if this.dashing: # check if dashing
            this.dash_cooldown -= 1 # count down by 1 each frame
            if this.dash_cooldown == 0: # check cooldown equals than 0 
                if this.stunned == False: # check not stunned
                    this.speed = this.saved_speed # set speed to saved speed
            if this.dash_cooldown <= -15: # continue past 0
                this.dashing = False # no longer dashing
                this.dash_cooldown = this.dash_timer # reset timer
    
    # Launch duckling
    def LaunchDuckling(this, force, speed, boid):
        if this.can_launch == False: return # make sure can launch duckling
        boid.vel = LimitMagnitude(force, speed)
        boid.max_speed = speed
        boid.in_flock = False
        this.can_launch = False
    def LaunchCooldown(this):
        if this.can_launch == False:
            this.launch_cooldown -= 1
            if this.launch_cooldown == 0:
                this.can_launch = True
                this.launch_cooldown = this.launch_timer

    ###---
    

    ###--- MAIN FUNCTIONS
    def AddForce(this, force=Vec2(0,0)):
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

    def CheckCollisions(this, colliders):
        collide_index = this.collide_rect.collidelist(colliders)
        return collide_index
    
    def CheckWallCollisions(this, walls):
        if this.stunned == True: return

        multiplier = this.CalculateCollisionRect()
        collide_index = this.collide_rect.collidelist(walls)
        if collide_index != -1:
            this.has_collision = True
            this.CollisionResponse(multiplier)
            return True
        
        this.has_collision = False
        return False
    
    def CalculateCollisionRect(this):
        this.collide_rect = this.rect
        multiplier = 5
        if (this.vel.x < 0 and this.vel.y > 0) or (this.vel.x < 0 and this.vel.y < 0) or (this.vel.x > 0 and this.vel.y < 0) or (this.vel.x > 0 and this.vel.y > 0) or (this.vel == Vec2(0,0)):
            this.collide_rect.width /= 2
            this.collide_rect.height /= 2 
            this.collide_rect.x += this.collide_rect.width/2
            this.collide_rect.y += this.collide_rect.height/2
            multiplier = 15

        return multiplier
    
    def CollisionResponse(this, multiplier):
        this.forces = Vec2(0,0)
        this.vel = (-this.last_vel) * multiplier
        this.speed = this.max_speed / 5
        this.stunned = True

    def Update(this):
        if this.stunned:
            this.stun_timer -= 1
            if this.stun_timer <= 0:
                this.speed = this.saved_speed
                this.stunned = False
                this.stun_timer = this.stun_length

        this.DashCooldown()
        this.LaunchCooldown()
        
        if this.vel != Vec2(0,0): # prevents angle from immediately going to zero when at a standstill, as we'd rather have it as the last angle when moving
            this.angle = (180/np.pi) * (np.arctan2(-this.vel.y, this.vel.x) - (90 * (np.pi/180))) # calculate the angle for the image to rotate
        accel = this.forces / this.mass
        this.vel = LimitMagnitude(this.vel + accel, this.max_speed / this.speed)
        this.pos += this.vel
        if this.vel != this.last_vel:
            this.last_vel = this.vel
            
        this.forces = Vec2(0,0) # reset forces vector

        this.img = py.transform.rotate(this.saved_img, this.angle)

    def Draw(this, window):
        this.rect = this.img.get_rect(center = this.screen_pos)
        temp_rect = window.blit(this.img, this.rect)
        return temp_rect
    
    ###---