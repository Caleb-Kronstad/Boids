import pygame as py
from pygame import Vector2 as Vec2
import numpy as np


def BoidSteeringForce(boid, flock, separation_distance, alignment_distance, cohesion_distance, separation_factor=1, alignment_factor=1, cohesion_factor=1):
    separationVector = Vec2(0,0)
    alignmentVector = Vec2(0,0)
    cohesionVector = Vec2(0,0)

    s_NearbyCount = 0
    a_NearbyCount = 0
    c_NearbyCount = 0

    for otherboid in flock:
        if otherboid == boid:
            continue

        distance = np.linalg.norm(otherboid.pos-boid.pos)

        if distance < separation_distance:
            posDiff = (boid.pos - otherboid.pos) / np.linalg.norm(boid.pos - otherboid.pos)
            separationForce = posDiff / distance
            separationVector += separationForce
            s_NearbyCount += 1

        if distance < alignment_distance:
            alignmentVector += Vec2(np.cos(otherboid.angle), np.sin(otherboid.angle))
            a_NearbyCount += 1

        if distance < cohesion_distance:
            cohesionVector += otherboid.pos
            c_NearbyCount += 1

    if s_NearbyCount > 0:
        separationVector /= s_NearbyCount
        separationVector *= separation_factor
    else:
        separationVector = Vec2(0,0)
    if a_NearbyCount > 0:
        alignmentVector /= a_NearbyCount
        alignmentVector *= alignment_factor
    else:
        alignmentVector = Vec2(0,0)
    if c_NearbyCount > 0:
        cohesionVector /= c_NearbyCount
        cohesionDirection = (cohesionVector - boid.pos) / np.linalg.norm(cohesionVector - boid.pos)
        cohesionVelocity = cohesionDirection * cohesion_factor
    else:
        cohesionVelocity = Vec2(0,0)

    return (separationVector + alignmentVector + cohesionVelocity)