#Code for the birds (what I've chosen the boids to be made of)
#import files
import pygame as py
import numpy as np
from colors import *
from ray import *

class Bird:
    def __init__(this, image, position, size, color, speed, angle, viewRange):
        this.position = position
        this.image = image
        this.size = size
        this.color = color
        this.speed = speed
        this.angle = angle
        this.viewRange = viewRange

    def Move(this):
        this.direction = np.array([np.cos(this.angle), np.sin(this.angle)])
        this.position = this.position + (this.direction * this.speed)

        #Don't let the birds go off the screen
        if (this.position[0] >= 1600):
            this.position = np.array([0, this.position[1]])
        elif (this.position[0] <= 0 - this.size[0]):
            this.position = np.array([1600, this.position[1]])
        elif (this.position[1] >= 900):
            this.position = np.array([this.position[0], 0])
        elif (this.position[1] <= 0 - this.size[1]):
            this.position = np.array([this.position[0], 900])

    def Rotate(this, angle):
        this.angle = angle

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
        window.blit(this.image, (this.position[0], this.position[1]))