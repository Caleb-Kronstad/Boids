##--- TEMPORARY CITATIONS ---
# Reynolds, Craig. “Boids.” Red3d, 1995, www.red3d.com/cwr/boids/. 
# Lague, Sebastian. “Coding Adventure: Boids.” YouTube, 26 Aug. 2019, www.youtube.com/watch?v=bqtqltqcQhw&t=118s. 
# Gavin. “How Do You Detect Where Two Line Segments Intersect?” Stack Overflow, 28 Dec. 2009, stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect. 
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
from door import *
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
    map = [
        # First area
        (0, 1000, 1500, 2000),
        (-1200, 1000, 1200, 1000),
        # Second area
        (1000, 0, 500, 1000),
        (-1200, -3000, 4000, 3000),
        (-2200, -4000, 1000, 2000),
        (2800, -500, 1000, 500),
        (3800, -500, 1000, 1500),
        # Third area
        (2300, -5000, 500, 2000),
        (-1200, -6000, 6000, 1000),
        (-2200, -7000, 1000, 2000),
        (4800, -7000, 1500, 3000),
        # Fourth area
        (2300, -8000, 500, 2000),
        (-1200, -10000, 4000, 2000),
        (-1200, -11000, 500, 1000),
        (-3700, -14000, 13000, 3000),
        (4300, -11000, 500, 3000),
        (2800, -8500, 1500, 500),
        # Fifth area
        (8800, -11000, 500, 7000),
        (6300, -7000, 2500, 500),
        (8000, -4000, 2500, 2000),
        # Sixth area (Boss)
        (2800, -1500, 3000, 500),
        (5300, -1000, 500, 5000),
        (4300, 3000, 5000, 5000)
    ]

    debug_colliders = True
    colliders = [
        (-1200, 0, 2200, 1000), #1
        (1500, 0, 2300, 3000), #2
        (-1200, -5000, 3500, 2000), #3
        (-2200, -5000, 1000, 1000), #4
        (-1200, -8000, 3500, 2000), #5
        (-3700, -11000, 2500, 4000), #6
        (-3700, -7000, 1500, 5000), #7
        (-3700, -2000, 2500, 4000), #8
        (-3700, 2000, 3700, 1000), #9
        (-1200, 3000, 2700, 1000), #10
        (1500, 3000, 2800, 6000), #11
        (3800, 1000, 1500, 2000), #12
        (4800, -500, 500, 1500), #13
        (2800, -1000, 2500, 500), #14
        (4300, 8000, 6000, 1000), #15
        (9300, 3000, 1000, 5000), #16
        (5800, -1500, 4500, 4500), #17
        (2800, -4000, 5200, 2500), #18
        (2800, -5000, 2000, 1000), #19
        (6300, -6500, 2500, 2500), #20
        (8000, -2000, 3500, 500), #21
        (10500, -4000, 1000, 2000), #22
        (9300, -14000, 1800, 10000), #23
        (-3700, -15000, 14800, 1000), #24
        (-4700, -15000, 1000, 5000), #25
        (-700, -11000, 5000, 1000), #26
        (2800, -10000, 1500, 1500), #27
        (4800, -11000, 4000, 4000), #28
        (2800, -8000, 2000, 2000), #29
    ]

    doors = [
        Door(1000, 900, 500, 100, boids_needed = 1), # first area to second
        
    ]

    circle_15px_img = cache.LoadImage('resources/circle_15px.png')
    circle_50px_img = cache.LoadImage('resources/circle_50px.png')
    blue_arrow_img = cache.LoadImage('resources/blue_arrow.png')
    yellow_arrow_img = cache.LoadImage('resources/yellow_arrow.png')
    water_bg_img = cache.LoadImage('resources/moving_water.png')
    walls_bg_img = cache.LoadImage('resources/walls.png')
    ducky_small_img = cache.LoadImage('resources/ducky_small.png')
    ducky_medium_img = cache.LoadImage('resources/ducky_medium.png')
    ducky_large_img = cache.LoadImage('resources/ducky_large.png')

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

    flock = Flock(Vec2(screen_width/2, screen_height - 300), Vec2(0,0), 5, 200, ducky_large_img)

    flock_rect = flock.Draw(window)

    bg_rects = []
    for bg in map:
        bg_rect = py.Rect(bg[0]/2, bg[1]/2, bg[2]/2, bg[3]/2)
        bg_rects.append(bg_rect)

    col_rects = []
    for col in colliders:
        col_rect = py.Rect(col[0]/2, col[1]/2, col[2]/2, col[3]/2)
        col_rects.append(col_rect)

    map_offset = [500, -700]
    for bg in bg_rects:
        bg.x += map_offset[0]
        bg.y += map_offset[1]
    for col in col_rects:
        col.x += map_offset[0]
        col.y += map_offset[1]
    for door in doors:
        door.rect.x += map_offset[0]
        door.rect.y += map_offset[1]

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
        if flock.stunned == False:
            if keys[py.K_w]:
                movement_vector.y -= flock.max_speed
            if keys[py.K_s]:
                movement_vector.y += flock.max_speed
            if keys[py.K_a]:
                movement_vector.x -= flock.max_speed
            if keys[py.K_d]:
                movement_vector.x += flock.max_speed 

        flock.Movement(movement_vector)

        # -- DRAW --
        window.fill(DARKGRAY)

        rounded_flock_velx = round(flock.vel.x)
        rounded_flock_vely = round(flock.vel.y)

        seen_rects = []
        for bg in bg_rects:
            bg.x -= rounded_flock_velx
            bg.y -= rounded_flock_vely

            if bg.x + bg.w >= 0 and bg.y + bg.h >= 0: #only render the backgrounds on screen to save performance
                py.draw.rect(window, CYAN, bg)
                seen_rects.append(bg)

        for col in col_rects:
            col.x -= rounded_flock_velx
            col.y -= rounded_flock_vely

            if debug_colliders and (col.x + col.w >= 0 and col.y + col.h >= 0):
                py.draw.rect(window, RED, col, 10)

        for door in doors:
            door.rect.x -= rounded_flock_velx
            door.rect.y -= rounded_flock_vely
            door.Draw(window)

        #water_rect = window.blit(water_bg_img, (0, bg_pos))
        #walls_rect = window.blit(walls_bg_img, (0, bg_pos))

        for x in sections.keys():
            for y in sections[x].keys():
                flock.boids = sections[x][y]
                for boid in sections[x][y].values():
                    
                    #Add forces to boid
                    if Normalize(flock.pos - boid.pos) < flock.range:
                        if not boid.in_flock:
                            boid.in_flock = True
                            flock.num_boids += 1

                        boid.max_speed = flock.max_speed
                        boid.alignment_enabled = False
                    else:
                        boid.max_speed = 4
                        boid.alignment_enabled = True
                        
                    boid.Flock(sections[x][y], flock)

                    #Update Boid
                    boid.Update()
                    boid.pos -= flock.vel
                    sections = boid.UpdateSections(sections)

                    #Draw Boid
                    direction_ray = Ray(boid.pos, boid.vel, 15)
                    #direction_ray.DebugDraw(window)
                    boid_rect = boid.Draw(window)

        flock.AddFlockCenterForce(movement_vector)
        
        # COLLISIONS
        flock.CheckWallCollisions(col_rects)
        flock.CheckDoorCollisions(doors)

        flock.Update()
        flock_rect = flock.Draw(window)

        # Draw text
        text_rect1 = window.blit(fps_text, (200, 50))
        text_rect2 = window.blit(flock_boid_num_text, (200, 100))
        py.display.update()



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
    add_boid_text = font_arial30.render("Press 'T' to add a boid", True, WHITE)
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
        fps_text = font_arial30.render("FPS: " + str(round(clock.get_fps())), True, WHITE)
        boid_count_text = font_arial30.render("BOIDS: " + str(boid_count), True, WHITE)

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