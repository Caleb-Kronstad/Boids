#imports
import pygame as py
from pygame import Vector2 as Vec2
import numpy as np
import random, sys

from boid import *
from helpfunctions import *

class Flock:
    def __init__(this, boids, center, direction, speed):
        this.boids = boids
        this.pos = center
        this.direction = direction
        this.speed = speed

        this.furthest_boid = this.FindFurthestBoidFromFlockCenter()

    def FindFurthestBoidFromFlockCenter(this):
        furthest_boid = None
        furthest_distance = 0
        for boid in this.boids.values():
            dist_from_center = Normalize(boid.pos - this.center)
            if dist_from_center > furthest_distance:
                furthest_distance = dist_from_center
                furthest_boid = boid

        return furthest_boid

    def Update(this):
        this.furthest_boid = this.FindFurthestBoidFromFlockCenter()