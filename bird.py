#Code for the birds (what I've chosen the boids to be made of)
#import files
import pygame as py
import numpy as np
from colors import *
from ray import *

class Bird:
    def __init__(this, position, size, color, speed, direction, viewRange):
        this.position = position
        this.size = size
        this.color = color
        this.speed = speed
        this.direction = direction
        this.viewRange = viewRange

    def StepPosition(this):
        this.position = this.position + (this.direction * this.speed)

        #Don't let the birds go off the screen
        if (this.position[0] >= 1600):
            this.position = np.array([0, this.position[1]])
        elif (this.position[0] <= 0):
            this.position = np.array([1600, this.position[1]])
        elif (this.position[1] >= 900):
            this.position = np.array([this.position[0], 0])
        elif (this.position[1] <= 0):
            this.position = np.array([this.position[0], 900])

    def CheckCollision(this, other):
        collisionX = (this.position[0] + this.size[0] >= other.position[0] and other.position[0] + other.size[0] >= this.position[0])
        collisionY = (this.position[1] + this.size[1] >= other.position[1] and other.position[1] + other.size[1] >= this.position[1])
        return (collisionX and collisionY)

    def AvoidObstacles(this, birds):
        goldenRatio = (1 + np.sqrt(5)) / 2
        numPoints = 300
        turnFraction = np.pi * 2 * goldenRatio
        
        for i in range(0, numPoints):
            dist = i / numPoints


    def ChangeSpeed(this, newSpeed = np.array([0,0])):
        this.speed = newSpeed

    def Update(this, window):
        rect = py.Rect(this.position[0], this.position[1], this.size[0], this.size[1])
        py.draw.rect(window, this.color, rect)