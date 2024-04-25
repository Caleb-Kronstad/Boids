##--- TEMPORARY CITATIONS ---
# https://www.cs.trinity.edu/~jhowland/cs2322/2d/2d/ 4/18/2024
# https://stackoverflow.com/questions/6247153/angle-from-2d-unit-vector 4/18/2024
# https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect 4/20/2024
# https://www.youtube.com/watch?v=HzR-9tfOJQo 4/20/2024
##---

#import libraries to be used
import pygame as py
from pygame import Vector2 as Vec2
import numpy as np
import random, sys, math

#import other files
from colors import *
from boid import *
from flock import *
from cache import *
from ray import *
from helpfunctions import *

py.init()
screen_width, screen_height = 1600, 900
py.display.set_caption("Boids")

menu_flag = True
performance_test_flag = False
game_flag = False

window_flags = py.DOUBLEBUF # | py.FULLSCREEN
window = py.display.set_mode((screen_width, screen_height), window_flags, 8)
clock = py.time.Clock()
fps = 60
cache = Cache()

font_arial30 = py.font.SysFont('Arial', 30)

## MAIN GAME

def MainGame(game):
    area_1 = { #x, y, width, height
        "start" : [0, 0, 1600, 900], #start
        "tutorial" : [-1000, -900, 2600, 900], #tutorial
    }
    area_2 = {
        "hallway-1" : [0, -900, 600, 1800], #hallway
        "puzzle-1" : [-5400, -3600, 6000, 2700], #puzzle
        "cell-1" : [-6200, -4500, 1600, 1800], #cell
        "hallway-2" : [600, -1800, 2000, 900], #hallway
        "cell-2" : [1800, -2700, 1000, 1400], #cell
        "hallway-3" : [600, -3600, 1200, 900] #hallway
    }
    area_3 = {
        "hallway-1" : [0, -1800, 600, 2700],
        "hallway-2" : [-800, -2700, 900, 2400],
        "puzzle-1" : [-2600, -2700, 1800, 2700],
        "puzzle-2" : [1600, -3100, 2000, 3100]
    }
    area_4 = {
        "hallway-1" : [0, -900, 600, 900],
        "puzzle-1" : [-3400, -2700, 4000, 1800]
    }
    area_5 = {
        "hallway-1" : [0, 0, 600, 900],
        "puzzle-1" : [-2000, -3000, 15000, 3000],
        "hallway-2" : [9000, 0, 1000, 2700],
        "hallway-3" : [4000, -2800, 4400, 600]
    }
    area_6 = {
        "hallway-1" : [0, 0, 800, 3400],
        "hallway-2" : [-4000, -2600, 4000, 900],
        "puzzle-1" : [-300, -3400, 2700, 1200]
    }

    areas = {
        1 : area_1,
        2 : area_2,
        3 : area_3,
        4 : area_4,
        5 : area_5,
        6 : area_6
    }

    circle_15px_img = cache.LoadImage('resources/circle_15px.png')
    circle_50px_img = cache.LoadImage('resources/circle_50px.png')
    blue_arrow_img = cache.LoadImage('resources/blue_arrow.png')
    yellow_arrow_img = cache.LoadImage('resources/yellow_arrow.png')
    water_bg_img = cache.LoadImage('resources/moving_water.png')
    walls_bg_img = cache.LoadImage('resources/walls.png')
    ducky_small_img = cache.LoadImage('resources/ducky_small.png')
    ducky_medium_img = cache.LoadImage('resources/ducky_medium.png')
    ducky_large_img = cache.LoadImage('resources/ducky_large.png')

    bg_pos = -900
    bg_speed = 1

    current_boid_img = ducky_small_img
    flock_params = FlockParams(50, 100, 200, 15, 1, 1)

    sections = {
        0: { 0: {}, 1: {}, 2: {} },
        1: { 0: {}, 1: {}, 2: {} },
        2: { 0: {}, 1: {}, 2: {} },
        3: { 0: {}, 1: {}, 2: {} }
    }

    for i in range(5):
        pos = Vec2(random.randint(500,600), random.randint(500,600))
        vel = Vec2(random.uniform(-1,1), random.uniform(-1,1))
        accel = Vec2(1,1)
        
        boid = Boid(pos, vel, accel, current_boid_img)
        sections[boid.section[0]][boid.section[1]][(boid.id)] = boid

    flock = Flock(Vec2(screen_width/2, screen_height - 300), Vec2(0,0), 3, 200, ducky_large_img)
    movement_vector = Vec2(0,0)
    movement_speed = [flock.max_speed, flock.max_speed]

    while game:
        clock.tick(fps)
        fps_text = font_arial30.render("FPS: " + str(round(clock.get_fps())), True, BLACK)
        flock_boid_num_text = font_arial30.render("Ducks Collected: " + str(flock.num_boids), True, BLACK)
        
        for e in py.event.get():
            if e.type == py.QUIT: 
                game = False
                sys.exit()

            #Get user input
            if e.type == py.KEYDOWN:
                key = e.key
            if e.type == py.KEYUP:
                key = e.key

        #Key input
        keys = py.key.get_pressed()

        #Movement force based on WASD keys pressed
        movement_vector = Vec2(0,0)
        if keys[py.K_w]:
            movement_vector.y -= movement_speed[1]
        if keys[py.K_s]:
            movement_vector.y += movement_speed[1]
        if keys[py.K_a]:
            movement_vector.x -= movement_speed[0]
        if keys[py.K_d]:
            movement_vector.x += movement_speed[0]
        flock.Movement(movement_vector)
            
        bg_pos += bg_speed
        if bg_pos > 0:
            bg_pos = -900
        elif bg_pos < -900:
            bg_pos = 0
        water_rect = window.blit(water_bg_img, (0, bg_pos))
        walls_rect = window.blit(walls_bg_img, (0, bg_pos))

        for x in sections.keys():
            for y in sections[x].keys():
                flock.boids = sections[x][y]
                for boid in sections[x][y].values():
                    
                    #Add forces to boid
                    if Normalize(flock.pos - boid.pos) < flock.range:
                        if not boid.in_flock:
                            boid.in_flock = True

                        boid.max_speed = flock.max_speed
                        boid.alignment_enabled = False
                    else:
                        boid.max_speed = 4
                        boid.alignment_enabled = True
                        
                    boid.Flock(sections[x][y], flock)

                    #Update
                    boid.Update()
                    sections = boid.UpdateSections(sections)

                    #Draw
                    direction_ray = SimpleRay(boid.pos, boid.vel, 15)
                    #direction_ray.Draw(window)
                    boid_rect = boid.Draw(window)

        flock.AddFlockCenterForce(movement_vector)
        flock.Update()
        flock_rect = flock.Draw(window)

        # Draw text
        text_rect1 = window.blit(fps_text, (200, 50))
        text_rect2 = window.blit(flock_boid_num_text, (200, 100))
        py.display.update(water_rect)

        

def Menu(menu, game, performance_test):
    play_button = py.Rect(screen_width/2 - 100, screen_height/2 - 100, 200, 50)
    play_text = font_arial30.render("Play", True, BLACK)

    test_button = py.Rect(screen_width/2 - 100, screen_height/2, 200, 50)
    test_text = font_arial30.render("Performance Test", True, BLACK)

    settings_button = py.Rect(screen_width/2 - 100, screen_height/2 + 100, 200, 50)
    settings_text = font_arial30.render("Settings", True, BLACK)

    exit_button = py.Rect(screen_width/2 - 100, screen_height/2 + 200, 200, 50)
    exit_text = font_arial30.render("Exit", True, BLACK)

    settings_open = False

    while menu:
        clock.tick(fps)
        window.fill(WHITE)

        for e in py.event.get():
            if e.type == py.QUIT: 
                menu = False
                sys.exit()

            if e.type == py.MOUSEBUTTONDOWN and e.button == 1:
                if exit_button.collidepoint(e.pos):
                    menu = False
                    sys.exit()
                elif play_button.collidepoint(e.pos):
                    menu = False
                    game = True
                    MainGame(game)
                elif test_button.collidepoint(e.pos):
                    menu = False
                    performance_test = True
                    PerformanceTest(performance_test)
                elif settings_button.collidepoint(e.pos):
                    settings_open = True

        py.draw.rect(window, CYAN, play_button)
        py.draw.rect(window, CYAN, test_button)
        py.draw.rect(window, CYAN, settings_button)
        py.draw.rect(window, CYAN, exit_button)
        window.blit(play_text, (play_button.x, play_button.y))
        window.blit(test_text, (test_button.x, test_button.y))
        window.blit(settings_text, (settings_button.x, settings_button.y))
        window.blit(exit_text, (exit_button.x, exit_button.y))

        py.display.update()

## PERFORMANCE TEST
def PerformanceTest(performance_test):
    blue_arrow_img = cache.LoadImage('resources/blue_arrow.png')
    add_boid_text = font_arial30.render("Press 'T' to add a boid", True, BLACK)
    boid_count = 0
    
    flock_params = FlockParams(50, 100, 200, 1, 1, 1)

    sections = {
        0: { 0: {}, 1: {}, 2: {} },
        1: { 0: {}, 1: {}, 2: {} },
        2: { 0: {}, 1: {}, 2: {} },
        3: { 0: {}, 1: {}, 2: {} }
    }

    for i in range(100):
        pos = Vec2(random.randint(0,screen_width), random.randint(0,screen_height))
        vel = Vec2(random.uniform(-1,1), random.uniform(-1,1))
        accel = Vec2(1,1)
        
        boid = Boid(pos, vel, accel, blue_arrow_img, 1, 0, 1600, False)
        sections[boid.section[0]][boid.section[1]][(boid.id)] = boid
        boid_count += 1

        t_down = False

    while performance_test:
        clock.tick(fps)
        fps_text = font_arial30.render("FPS: " + str(round(clock.get_fps())), True, BLACK)
        boid_count_text = font_arial30.render("BOIDS: " + str(boid_count), True, BLACK)

        for e in py.event.get():
            if e.type == py.QUIT: 
                performance_test = False
                sys.exit()
            
            if e.type == py.KEYDOWN:
                if e.key == py.K_t and t_down == False:
                    t_down = True
                    pos = Vec2(random.randint(0,screen_width), random.randint(0,screen_height))
                    vel = Vec2(random.uniform(-1,1), random.uniform(-1,1))
                    accel = Vec2(1,1)
                    
                    boid = Boid(pos, vel, accel, blue_arrow_img, 1, 0, 1600, False)
                    sections[boid.section[0]][boid.section[1]][(boid.id)] = boid
                    boid_count +=1 
            
            if e.type == py.KEYUP:
                if e.key == py.K_t:
                    t_down = False

        window.fill(DARKGRAY)
        
        for x in sections.keys():
            for y in sections[x].keys():
                for boid in sections[x][y].values():
                    #Add forces to boid
                    boid.Flock(sections[x][y], flock_params = flock_params)
                    #Update
                    boid.Update()
                    sections = boid.UpdateSections(sections)
                    #Draw
                    #direction_ray = SimpleRay(boid.pos, boid.vel, 15)
                    #direction_ray.Draw(window)
                    boid_rect = boid.Draw(window)

        # Draw text
        window.blit(fps_text, (100, 50))
        window.blit(boid_count_text, (100, 100))
        window.blit(add_boid_text, (100, 150))
        py.display.update()



## call functions to run game
Menu(menu_flag, game_flag, performance_test_flag)
py.quit()