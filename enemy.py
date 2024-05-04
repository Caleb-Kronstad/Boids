#imports
import pygame as py
from pygame import Vector2 as Vec2
from helpfunctions import *
import numpy as np

class Enemy:
    def __init__(this, pos, vel,  accel, health, img, despawn_img, max_speed=4, max_force=0.2, mass=1):
        this.pos = pos
        this.vel = vel
        this.accel = accel
        this.mass = mass
        this.health = health
        
        this.img = img
        this.despawn_img = despawn_img
        this.saved_img = img
        this.rect = this.img.get_rect(center = this.pos)

        this.max_speed = max_speed
        this.max_force = max_force

        this.size_multiplier = 1

        this.forces = accel * mass

        this.hit_player = False
        this.despawn_timer = 30

    def AddForce(this, force=Vec2(0,0)):
        this.forces += force

    def CheckCollisions(this, colliders):
        col_index = this.rect.collidelist(colliders)
        if col_index != -1:
            this.forces = Vec2(0,0)

    def Update(this, flock):
        this.img = py.transform.rotate(this.saved_img, (180/np.pi) * (np.arctan2(-this.vel.y, this.vel.x) - (90 * (np.pi/180))))

        dist_from_flock = Normalize(flock.screen_pos - this.pos)
        if dist_from_flock > 200:
            this.size_multiplier = 1
            this.AddForce(SetMagnitude(LimitMagnitude(flock.screen_pos - this.pos, this.max_speed), this.max_speed))
        else:
            if this.size_multiplier < 5: this.size_multiplier += 1
            elif this.size_multiplier >= 5: this.size_multiplier -= 4
            this.forces = Vec2(0,0)
            this.vel = Vec2(0,0)
            this.hit_player = True
            this.img = py.transform.scale(this.despawn_img, (this.despawn_img.get_width() * this.size_multiplier, this.despawn_img.get_height() * this.size_multiplier))
    
        if this.hit_player == False:
            this.accel = this.forces / this.mass
            this.vel = LimitMagnitude(this.vel + this.accel, this.max_speed)
            this.pos += this.vel
        else:
            this.despawn_timer -= 1
        this.pos -= flock.vel
        this.last_vel = this.vel
        this.forces = Vec2(0,0) # reset forces for next frame

    def Draw(this, window):
        this.rect = this.img.get_rect(center = this.pos)
        temp_rect = window.blit(this.img, this.rect)
        return temp_rect