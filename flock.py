#imports
import pygame as py
from pygame import Vector2 as Vec2
import numpy as np

from boid import *
from helpfunctions import *

class FlockParams(): # Params for flock calculations
    def __init__(this, separation_distance = 50, alignment_distance = 100, cohesion_distance = 200, separation_factor = 1, alignment_factor = 1, cohesion_factor = 1):
        this.separation_distance = separation_distance # max distance for separation calculation to take place
        this.alignment_distance = alignment_distance # max distance for aligment calculation to take place
        this.cohesion_distance = cohesion_distance # max distance for cohesion calculation to take place
        this.separation_factor = separation_factor # multiplier for separation calculation
        this.alignment_factor = alignment_factor # multiplier for alignment calculation
        this.cohesion_factor = cohesion_factor # multiplier for cohesion calculation

class Flock: # Player

    ###--- INIT FUNCTION

    def __init__(this, pos, vel, speed, range, health, img, max_boids=25, mass=1):
        # initialize member variables
        this.pos = pos # position of the player, a constant
        this.speed = speed # speed of the player
        this.saved_speed = speed # saved speed of the player
        this.max_speed = 50 # max speed of the player
        this.vel = LimitMagnitude(vel, this.max_speed) # velocity of the player
        this.last_vel = vel # last velocity of the player
        this.range = range # boid range
        this.mass = mass # mass of the player

        this.forces = Vec2(0,0) # forces of the player
        this.angle = np.degrees(np.arctan2(-this.vel.y, this.vel.x) - np.radians(90)) # player rotation angle

        this.coins = 0 # coins collected
        this.health = health # current health
        this.boid_damage = 1 # amount of damage boids do to enemies
        this.max_boids = max_boids # number of maximum boids
        this.num_boids = 0 # number of boids
        this.has_collision = False # collision bool

        this.img = img # player img
        this.saved_img = img # also player img

        this.rect = this.img.get_rect(center = this.pos) # player rect
        this.CalculateCollisionRect() # collision rect calculation

        this.stunned = False # stunned bool
        this.stun_timer = 30 # stun timer
        this.stun_length = this.stun_timer # stun length

        #Upgrades
        this.dashing = False # dashing bool
        this.dash_cooldown = 15 # dashing cooldown
        this.dash_timer = this.dash_cooldown # dashing timer

        this.can_launch = True # launch bool
        this.launch_cooldown = 15 # launch cooldown
        this.launch_timer = this.launch_cooldown # launch timer
        
    ###---


    ###--- UPGRADES

    def Dash(this, force): # Dash
        if this.dashing: return # make sure not already dashing
        this.AddForce(force) # add dashing force
        this.speed = this.max_speed / 15 # change speed 
        this.dashing = True # dashing flag set to true
    def LaunchDuckling(this, force, speed, boid): # Launch duckling
        if this.can_launch == False: return # make sure can launch duckling
        boid.vel = LimitMagnitude(force, speed) # change boid velocity to direction of launch force
        boid.max_speed = speed # change the max speed of the boid
        boid.in_flock = False # take the boid out of the flock
        this.can_launch = False # can't launch duckling anymore

    # Cooldowns
    def StunCooldown(this, ts): # cooldown for stun from collisions
        if this.stunned: # check if stunned
            this.stun_timer -= 1 * ts # count down each frame
            if this.stun_timer <= 0: # 
                this.speed = this.saved_speed
                this.stunned = False
                this.stun_timer = this.stun_length
    def DashCooldown(this, ts):
        if this.dashing: # check if dashing
            this.dash_cooldown -= 1 * ts # count down each frame
            if this.dash_cooldown <= 0: # check cooldown equals than 0 
                if this.stunned == False: # check not stunned
                    this.speed = this.saved_speed # set speed to saved speed
            if this.dash_cooldown <= -15: # continue past 0
                this.dashing = False # no longer dashing
                this.dash_cooldown = this.dash_timer # reset timer
    def LaunchCooldown(this, ts):
        if this.can_launch == False:
            this.launch_cooldown -= 1 * ts
            if this.launch_cooldown <= 0:
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
        this.collide_rect = this.rect # set collide rect to this rect
        multiplier = 5 # set multiplier for collision velocity
        if (this.vel.x < 0 and this.vel.y > 0) or (this.vel.x < 0 and this.vel.y < 0) or (this.vel.x > 0 and this.vel.y < 0) or (this.vel.x > 0 and this.vel.y > 0) or (this.vel == Vec2(0,0)): # check if player is moving diagonally
            this.collide_rect.width /= 2 # divide rect width by 2
            this.collide_rect.height /= 2 # divide rect height by 2
            this.collide_rect.x += this.collide_rect.width/2 # add rect width/2 to rect x
            this.collide_rect.y += this.collide_rect.height/2 # add rect height/2 to rect y
            multiplier = 15 # change multiplier
        return multiplier
    
    def CollisionResponse(this, multiplier):
        this.forces = Vec2(0,0) # set forces to 0
        this.vel = (-this.last_vel) * multiplier # turn player around and send other way
        this.speed = this.max_speed / 5 # set player speed
        this.stunned = True # player is stunned

    def Update(this, ts):
        this.StunCooldown(ts) # stun cooldown
        this.DashCooldown(ts) # dash cooldown
        this.LaunchCooldown(ts) # launch cooldown
        
        if this.vel != Vec2(0,0): # prevents angle from immediately going to zero when at a standstill, as we'd rather have it as the last angle when moving
            this.angle = (180/np.pi) * (np.arctan2(-this.vel.y, this.vel.x) - (90 * (np.pi/180))) # calculate the angle for the image to rotate
        accel = this.forces / this.mass # calculate acceleration
        this.vel = LimitMagnitude(this.vel + accel * ts, this.max_speed / this.speed)
        # don't update position because the flock/player stays in the middle of the screen at one position
        if this.vel != this.last_vel: # check if velocity isn't equal to last velocity
            this.last_vel = this.vel # set last velocity equal to velocity
            
        this.forces = Vec2(0,0) # reset forces vector

        this.img = py.transform.rotate(this.saved_img, this.angle) # rotate the image based on angle

    def Draw(this, window):
        this.rect = this.img.get_rect(center = this.pos) # change rect based on image
        temp_rect = window.blit(this.img, this.rect) # draw onto screen
        return temp_rect # return rect
    
    ###---