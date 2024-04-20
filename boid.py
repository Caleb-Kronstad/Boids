#imports
import pygame as py
from pygame import Vector2 as Vec2
import random
import numpy as np
import sys
from colors import *
from ray import *

def Limit(vector, limit):
    magnitude = np.linalg.norm(vector)
    if magnitude > limit:
        normalized_vector = vector / magnitude
        limited_vector = normalized_vector * limit
        return limited_vector
    else:
        return vector
    
def SetMag(vector, magnitude):
    if (np.linalg.norm(vector) > 0):
        normalized_vector = vector / np.linalg.norm(vector)
    else:
        return Vec2(0,0)
    scaled_vector = normalized_vector * magnitude
    return scaled_vector

def FindCurrentSection(boid):
    if boid.pos.x >= 0 and boid.pos.x < 400:
        xs = 0
    elif boid.pos.x >= 400 and boid.pos.x < 800:
        xs = 1
    elif boid.pos.x >= 800 and boid.pos.x < 1200:
        xs = 2
    elif boid.pos.x >= 1200 and boid.pos.x <= 1600:
        xs = 3
    else:
        xs = 0
        print("error finding x selection")

    if boid.pos.y >= 0 and boid.pos.y < 300:
        ys = 0
    elif boid.pos.y >= 300 and boid.pos.y < 600:
        ys = 1
    elif boid.pos.y >= 600 and boid.pos.y <= 900:
        ys = 2
    else:
        ys = 0
        print("error finding y selection")
    
    return [xs,ys]

class FlockParams():
    def __init__(this, separation_distance = 50, alignment_distance = 100, cohesion_distance = 200, separation_factor = 1, alignment_factor = 1, cohesion_factor = 1):
        this.separation_distance = separation_distance
        this.alignment_distance = alignment_distance
        this.cohesion_distance = cohesion_distance
        this.separation_factor = separation_factor
        this.alignment_factor = alignment_factor
        this.cohesion_factor = cohesion_factor

class Boid:
    def __init__(this, pos, vel, accel, img, mass=1):
        this.id = random.randint(-sys.maxsize-1, sys.maxsize)

        this.pos = pos
        this.accel = accel
        this.mass = mass
        
        this.vel = vel / np.linalg.norm(vel)

        this.max_force = 0.2
        this.max_speed = 4

        this.img = img
        this.saved_img = img

        this.forces = accel * mass

        this.section = FindCurrentSection(this)
        this.previous_section = this.section

    def Flock(this, boids, flock_params = FlockParams()):
        this.accel = Vec2(0,0)
        alignment_force = Vec2(0,0)
        cohesion_force = Vec2(0,0)
        separation_force = Vec2(0,0)
        alignment_dist = flock_params.alignment_distance
        cohesion_dist = flock_params.cohesion_distance
        separation_dist = flock_params.separation_distance
        alignment_neighbors = 0
        cohesion_neighbors = 0
        separation_neighbors = 0

        for other in boids.values():
            if other == this: continue

            dist = np.linalg.norm(other.pos - this.pos)

            if dist < alignment_dist:
                alignment_force += (other.vel * flock_params.alignment_factor)
                alignment_neighbors += 1

            if dist < cohesion_dist:
                cohesion_force += (other.pos * flock_params.cohesion_factor)
                cohesion_neighbors += 1

            if dist < separation_dist:
                diff = this.pos - other.pos
                diff *= (1 / dist)
                separation_force += (diff * flock_params.separation_factor)
                separation_neighbors += 1
        
        if alignment_neighbors > 0:
            alignment_force /= alignment_neighbors
            alignment_force = SetMag(alignment_force, this.max_speed)
            alignment_force -= this.vel
            alignment_force = Limit(alignment_force, this.max_force)

        if cohesion_neighbors > 0:
            cohesion_force /= cohesion_neighbors
            cohesion_force -= this.pos
            cohesion_force = SetMag(cohesion_force, this.max_speed)
            cohesion_force -= this.vel
            cohesion_force = Limit(cohesion_force, this.max_force)
        
        if separation_neighbors > 0:
            separation_force /= separation_neighbors
            separation_force = SetMag(separation_force, this.max_speed)
            separation_force -= this.vel
            separation_force = Limit(separation_force, this.max_force)

        this.forces = cohesion_force + alignment_force + separation_force

    def UpdateSections(this, sections):
        temp_sections = sections
        if this.section != this.previous_section and this.id in temp_sections[this.previous_section[0]][this.previous_section[1]]:
            temp_sections = {x: {y: dict(sections[x][y]) for y in sections[x]} for x in sections}
            temp_sections[this.previous_section[0]][this.previous_section[1]].pop(this.id)
            temp_sections[this.section[0]][this.section[1]].update({this.id: this})

        return temp_sections

    def Update(this):
        this.accel = this.forces / this.mass
        this.vel = Limit(this.vel + this.accel, this.max_speed)
        this.pos += this.vel

        if (this.pos.x > 1600):
            this.pos.x = 0
        elif (this.pos.x < 0):
            this.pos.x = 1600
        elif (this.pos.y > 900):
            this.pos.y = 0
        elif (this.pos.y < 0):
            this.pos.y = 900

        this.section = FindCurrentSection(this)

    def Draw(this, window):
        #this.img = py.transform.rotate(this.saved_img, np.degrees(np.arctan2(this.vel.y, this.vel.x)))
        this.rect = this.img.get_rect(center = this.pos)
        window.blit(this.img, this.rect)