#imports
import pygame as py
from pygame import Vector2 as Vec2
import numpy as np
import math, random, sys

from colors import *
from ray import *
from helpfunctions import *

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
        
        this.vel = vel / Normalize(vel)

        this.max_force = 0.2
        this.max_speed = 4

        this.img = img
        this.saved_img = img

        this.forces = accel * mass

        this.section = FindBoidSection(this)
        this.previous_section = this.section

    def Flock(this, boids, flock_params = FlockParams()):
        alignment_force = Vec2(0,0)
        cohesion_force = Vec2(0,0)
        separation_force = Vec2(0,0)
        alignment_neighbors = 0
        cohesion_neighbors = 0
        separation_neighbors = 0

        for other in boids.values():
            if other == this: continue

            dist = Normalize(other.pos-this.pos)

            if dist < flock_params.alignment_distance:
                alignment_force += (other.vel * flock_params.alignment_factor)
                alignment_neighbors += 1

            if dist < flock_params.cohesion_distance:
                cohesion_force += (other.pos * flock_params.cohesion_factor)
                cohesion_neighbors += 1

            if dist < flock_params.separation_distance:
                diff = this.pos - other.pos
                diff *= (1 / dist)
                separation_force += (diff * flock_params.separation_factor)
                separation_neighbors += 1
        
        if alignment_neighbors > 0:
            alignment_force /= alignment_neighbors
            alignment_force = SetMagnitude(alignment_force, this.max_speed)
            alignment_force -= this.vel
            alignment_force = LimitMagnitude(alignment_force, this.max_force)

        if cohesion_neighbors > 0:
            cohesion_force /= cohesion_neighbors
            cohesion_force -= this.pos
            cohesion_force = SetMagnitude(cohesion_force, this.max_speed)
            cohesion_force -= this.vel
            cohesion_force = LimitMagnitude(cohesion_force, this.max_force)
        
        if separation_neighbors > 0:
            separation_force /= separation_neighbors
            separation_force = SetMagnitude(separation_force, this.max_speed)
            separation_force -= this.vel
            separation_force = LimitMagnitude(separation_force, this.max_force)

        this.AddForce(cohesion_force)
        this.AddForce(alignment_force)
        this.AddForce(separation_force)

    def AddForce(this, force = Vec2(0,0)):
        this.forces += force

    def UpdateSections(this, sections):
        temp_sections = sections
        if this.section != this.previous_section and this.id in temp_sections[this.previous_section[0]][this.previous_section[1]]:
            temp_sections = {x: {y: dict(sections[x][y]) for y in sections[x]} for x in sections}
            temp_sections[this.previous_section[0]][this.previous_section[1]].pop(this.id)
            temp_sections[this.section[0]][this.section[1]].update({this.id: this})
            this.previous_section = this.section

        return temp_sections

    def Update(this):
        this.accel = this.forces / this.mass
        this.vel = LimitMagnitude(this.vel + this.accel, this.max_speed)
        this.pos += this.vel
        this.forces = Vec2(0,0) # reset forces for next frame

        this.img = py.transform.rotate(this.saved_img, np.degrees(np.arctan2(-this.vel.y, this.vel.x) - 90)) # rotate boid image -- due to py's skewed coordinate system the rotation has to be altered slightly (hence the negative y axis and minus 90)

        if (this.pos.x > 1425):
            this.pos.x = 175
        elif (this.pos.x < 175):
            this.pos.x = 1425
        elif (this.pos.y > 900):
            this.pos.y = 0
        elif (this.pos.y < 0):
            this.pos.y = 900

        this.section = FindBoidSection(this)

    def Draw(this, window):
        this.rect = this.img.get_rect(center = this.pos)
        drawn_rect = window.blit(this.img, this.rect)
        return drawn_rect