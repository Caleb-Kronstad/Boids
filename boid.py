#import files
import pygame as py
import numpy as np
from colors import *
from ray import *

#Boid class
class Boid:
    def __init__(this, image, position, size, direction, speed, viewRange, ray):
        this.position = position
        this.image = image
        this.size = size
        this.direction = direction
        this.speed = speed
        this.viewRange = viewRange
        this.ray = ray
        this.rect = py.Rect(this.position[0], this.position[1], this.size[0], this.size[1])

    def Move(this):
        this.position = this.position + (this.direction * this.speed)

        this.rect = py.Rect(this.position[0], this.position[1], this.size[0], this.size[1])
        this.ray.Cast(this.position + (this.size/2), this.direction)

        #Don't let the boids go off the screen
        if (this.position[0] >= 1600):
            this.direction = this.direction * -1
        elif (this.position[0] <= 0 - this.size[0]):
            this.direction = this.direction * -1
        elif (this.position[1] >= 900):
            this.direction = this.direction * -1
        elif (this.position[1] <= 0 - this.size[1]):
            this.direction = this.direction * -1

    def CheckCollision(this, otherRect):
        hasCollision = this.ray.rect.colliderect(otherRect)
        return hasCollision

    def ChangeSpeed(this, newSpeed = np.array([0,0])):
        this.speed = newSpeed

    def Draw(this, window):
        py.draw.rect(window, CYAN, this.rect)
        #window.blit(this.image, (this.position[0], this.position[1]))