#imports
import pygame as py
from pygame import Vector2 as Vec2
import numpy as np

from helpfunctions import *

class EnemyParams: # params used to create enemy
    def __init__(this, type, img, despawn_img, attack_img, attack_range, speed, health, damage, value):
        this.type = type # enemy type
        this.img = img # enemy img
        this.despawn_img = despawn_img # img used for despawn animation
        this.attack_img = attack_img # img used for attack animation
        this.attack_range = attack_range # how close to attack player
        this.health = health # maximum health
        this.damage = damage # damage to player
        this.value = value # coins awarded to player when defeated
        this.speed = speed # enemy speed

def SpawnEnemy(type_params):
    randx, randy = GenerateSpawnPointOffMap() # generates random x and y points off the visible part of the screen
    pos = Vec2(randx,randy) # sets position using random x and y points
    vel = Vec2(0,0) # sets velocity
    accel = Vec2(0,0) # sets acceleration

    return Enemy(type_params.type, pos, vel, accel, type_params.health, type_params.damage, type_params.value, type_params.attack_range, type_params.img, type_params.attack_img, type_params.despawn_img, type_params.speed) # returns Enemy type

def SpawnWave(enemies_array, num_enemies, type_params): # Spawn a wave of enemies based on type and number
    for i in range(num_enemies):
        enemy = SpawnEnemy(type_params)
        enemies_array.append(enemy)
    return enemies_array

class Enemy:
    def __init__(this, type, pos, vel, accel, health, damage, value, attack_range, img, attack_img, despawn_img, max_speed=4, max_force=0.2, mass=1):
        this.type = type
        this.pos = pos
        this.vel = vel
        this.accel = accel
        this.mass = mass
        this.health = health
        this.damage = damage
        this.value = value
        this.attack_range = attack_range

        this.can_damage = True
        
        this.img = img
        this.attack_img = attack_img
        this.despawn_img = despawn_img
        this.saved_img = img
        this.rect = this.img.get_rect(center = this.pos)

        this.max_speed = max_speed
        this.max_force = max_force

        this.size_multiplier = 1

        this.forces = accel * mass

        this.hit_player = False
        this.despawn_timer = 30

        this.boss_attack_cd = 120
        this.boss_attack_timer = this.boss_attack_cd

    def Separate(this, enemies): # Separate enemies from eachother based on other enemies surrounding
        separation_force = Vec2(0,0)
        separation_dist = 100
        separation_neighbors = 0

        for other in enemies:
            if other == this: continue

            dist = Normalize(other.pos - this.pos)
            if dist < separation_dist:
                diff = this.pos - other.pos
                if dist == 0:
                    dist = 1
                diff *= 1 / dist
                separation_force += diff
                separation_neighbors += 1
                
            if separation_neighbors > 0:
                separation_force /= separation_neighbors
                separation_force = SetMagnitude(separation_force, this.max_speed)
                separation_force -= this.vel
                separation_force = LimitMagnitude(separation_force, this.max_force) * 10

            this.AddForce(separation_force)

    def TypeCheck(this, ts, dist_from_flock, flock): # check enemy type to invoke different responses
        if this.type == "sploder":
            if dist_from_flock > this.attack_range and this.hit_player == False:
                this.AddForce(LimitMagnitude((flock.pos - this.pos) * this.max_speed, this.max_speed))
            else:
                this.hit_player = True
                this.forces = Vec2(0,0)
                this.vel = Vec2(0,0)

        if this.type == "boss":
            if dist_from_flock > this.attack_range and this.hit_player == False:
                this.AddForce(LimitMagnitude((flock.pos - this.pos) * this.max_speed, this.max_speed))
            else:
                this.hit_player = True
                this.forces = Vec2(0,0)
                this.vel = Vec2(0,0)

            if this.can_damage == False:
                this.boss_attack_cd -= 1 * ts
                if this.boss_attack_cd <= 0:
                    this.can_damage = True
                    this.boss_attack_cd = this.boss_attack_timer

    def AddForce(this, force=Vec2(0,0)): # add force to entity
        this.forces += force

    def CheckCollisions(this, colliders): # check collisions with collider
        col_index = this.rect.collidelist(colliders)
        if col_index != -1:
            this.forces = Vec2(0,0)

    def Update(this, ts, flock): # Update enemy physics and position
        this.img = py.transform.rotate(this.saved_img, (180/np.pi) * (np.arctan2(-this.vel.y, this.vel.x) - (90 * (np.pi/180))))

        dist_from_flock = Normalize(flock.pos - this.pos)
        this.TypeCheck(ts, dist_from_flock, flock)
    
        if this.hit_player == False:
            this.accel = this.forces / this.mass
            this.vel = LimitMagnitude(this.vel + this.accel * ts, this.max_speed)
            this.pos += this.vel * ts
        elif this.hit_player == True:
            if this.size_multiplier < 5: this.size_multiplier += 1 * ts
            elif this.size_multiplier >= 5: this.size_multiplier -= 4 * ts

            this.img = py.transform.scale(this.despawn_img, (this.despawn_img.get_width() * this.size_multiplier, this.despawn_img.get_height() * this.size_multiplier))

            this.despawn_timer -= 1 * ts

        this.pos -= flock.vel * ts
        this.last_vel = this.vel
        this.forces = Vec2(0,0) # reset forces for next frame

    def Draw(this, window):
        this.rect = this.img.get_rect(center = this.pos)
        temp_rect = window.blit(this.img, this.rect)
        return temp_rect