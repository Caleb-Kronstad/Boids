##--- TEMPORARY CITATIONS ---
# https://www.cs.trinity.edu/~jhowland/cs2322/2d/2d/
# https://stackoverflow.com/questions/6247153/angle-from-2d-unit-vector
# https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
# https://www.youtube.com/watch?v=HzR-9tfOJQo
##---

#import libraries to be used
import pygame as py
from pygame import Vector2 as Vec2
import numpy as np
import random, sys

#import other files
from colors import *
from boid import *
from cache import *
from ray import *
from helpfunctions import *

py.init()
screen_width, screen_height = 1600, 900
py.display.set_caption("Boids")
window_flags = py.DOUBLEBUF # | py.FULLSCREEN
window = py.display.set_mode((screen_width, screen_height), window_flags, 8)

clock = py.time.Clock()
fps = 60
cache = Cache()

fps_font_color = BLACK
font_arial30 = py.font.SysFont('Arial', 30)

circle_15px_img = cache.LoadImage('resources/circle_15px.png')
circle_50px_img = cache.LoadImage('resources/circle_50px.png')
blue_arrow_img = cache.LoadImage('resources/blue_arrow.png')
yellow_arrow_img = cache.LoadImage('resources/yellow_arrow.png')
water_bg_img = cache.LoadImage('resources/moving_water.png')
walls_bg_img = cache.LoadImage('resources/walls.png')
ducky_small_img = cache.LoadImage('resources/ducky_small.png')
ducky_medium_img = cache.LoadImage('resources/ducky_medium.png')
ducky_large_img = cache.LoadImage('resources/ducky_large.png')

water_bg_pos = -2700
water_bg_speed = 0

current_boid_img = ducky_small_img
flock_params = FlockParams(50, 100, 200, 1, 1, 1)

sections = {
    0: { 0: {}, 1: {}, 2: {} },
    1: { 0: {}, 1: {}, 2: {} },
    2: { 0: {}, 1: {}, 2: {} },
    3: { 0: {}, 1: {}, 2: {} }
}

for i in range(200):
    pos = Vec2(random.randint(175,screen_width-175), random.randint(0,screen_height))
    vel = Vec2(random.uniform(-1,1), random.uniform(-1,1))
    accel = Vec2(5,5)
    
    boid = Boid(pos, vel, accel, current_boid_img)
    sections[boid.section[0]][boid.section[1]][(boid.id)] = boid

input_force = Vec2(1,5)

while 1:
    clock.tick(fps)
    fps_text = font_arial30.render("FPS: " + str(round(clock.get_fps())), True, fps_font_color)
    
    for e in py.event.get():
        if e.type == py.QUIT or (e.type == py.KEYDOWN and e.key == py.K_ESCAPE): 
            sys.exit()

        #Get user input
        if e.type == py.KEYDOWN:
            key = e.key
        if e.type == py.KEYUP:
            key = e.key

    #Key input
    keys = py.key.get_pressed()

    #Movement force based on WASD keys pressed
    input_vector = Vec2(0,0)
    if keys[py.K_w]:
        input_vector.y -= input_force.y
    if keys[py.K_s]:
        input_vector.y += input_force.y
    if keys[py.K_a]:
        input_vector.x -= input_force.x
    if keys[py.K_d]:
        input_vector.x += input_force.x

    water_bg_pos += water_bg_speed
    if water_bg_pos > 0:
        water_bg_pos = -2700
    water_rect = window.blit(water_bg_img, (0, water_bg_pos))
    walls_rect = window.blit(walls_bg_img, (0,0))

    for x in sections.keys():
        for y in sections[x].keys():
            for boid in sections[x][y].values():
                
                #Add forces to boid
                boid.Flock(sections[x][y])
                boid.AddForce(input_vector)

                #Update
                boid.Update()
                sections = boid.UpdateSections(sections)

                #Draw
                direction_ray = SimpleRay(boid.pos, boid.vel, 15)
                #direction_ray.Draw(window)
                boid_rect = boid.Draw(window)


    # Draw text
    text_rect = window.blit(fps_text, (200, 80))
    py.display.update(water_rect)

py.quit()