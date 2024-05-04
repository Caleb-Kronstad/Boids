##--- TEMPORARY CITATIONS ---
# Reynolds, Craig. “Boids.” Red3d, 1995, www.red3d.com/cwr/boids/. 
# Lague, Sebastian. “Coding Adventure: Boids.” YouTube, 26 Aug. 2019, www.youtube.com/watch?v=bqtqltqcQhw&t=118s. 
# Gavin. “How Do You Detect Where Two Line Segments Intersect?” Stack Overflow, 28 Dec. 2009, stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect. 
##---

### -- IMPORTANT --
# - The code for the performance test is much easier to understand (less complex) and is better for observing the specifics of implementing boids in code
# - The performance test is also better optimized as it utilizes things such as dictionaries for the boids rather than lists, which have much faster lookups

###

#import libraries to be used
import pygame as py
from pygame import Vector2 as Vec2
import numpy as np
import random, sys, math

#import other files
from colors import *
from boid import *
from flock import *
from enemy import *
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
    circle_15px_img = cache.LoadImage('resources/circle_15px.png')
    circle_50px_img = cache.LoadImage('resources/circle_50px.png')
    blue_arrow_img = cache.LoadImage('resources/blue_arrow.png')
    yellow_arrow_img = cache.LoadImage('resources/yellow_arrow.png')
    ducky_small_img = cache.LoadImage('resources/ducky_small.png')
    ducky_medium_img = cache.LoadImage('resources/ducky_medium.png')
    ducky_large_img = cache.LoadImage('resources/ducky_large.png')

    map = [
        py.Rect(-1000, -1000, 2000, 2000),
    ]

    debug_colliders = True
    colliders = [
        py.Rect(-1000, -2000, 2000, 1000), #top
        py.Rect(-1000, 1000, 2000, 1000), #bottom
        py.Rect(-2000, -1000, 1000, 2000), #left
        py.Rect(1000, -1000, 1000, 2000), #right
    ]

    map_offset = [1000, 0]
    for bg in map:
        bg.x += map_offset[0]
        bg.y += map_offset[1]
    for col in colliders:
        col.x += map_offset[0]
        col.y += map_offset[1]

    flock_params = FlockParams(separation_distance = 50, alignment_distance = 100, cohesion_distance = 200, separation_factor = 1, alignment_factor = 1, cohesion_factor = 1)

    boids = []
    removed_boids = []

    flock = Flock(Vec2(screen_width/2, screen_height/2), Vec2(0,0), 10, 200, ducky_large_img)

    for i in range(25):
        pos = Vec2(flock.screen_pos.x + random.randint(-100,100), flock.screen_pos.y + random.randint(-100,100))
        vel = Vec2(random.uniform(-1,1), random.uniform(-1,1))
        accel = Vec2(1,1)
        
        boid = Boid(pos, vel, accel, ducky_small_img)
        boid.in_flock = True
        boids.append(boid)

    enemies = []

    for i in range(2):
        pos = Vec2(random.randint(200,400), random.randint(200,400))
        vel = Vec2(0,0) #Vec2(random.uniform(-1,1), random.uniform(-1,1))
        accel = Vec2(0,0)

        enemy = Enemy(pos, vel, accel, 1, circle_50px_img, circle_50px_img)
        enemies.append(enemy)

    flock.num_boids = len(boids)
    flock.Draw(window)

    while game:
        clock.tick(fps)
        fps_text = font_arial30.render("FPS: " + str(round(clock.get_fps())), True, BLACK)
        flock_boid_num_text = font_arial30.render("Ducks Collected: " + str(flock.num_boids), True, BLACK)

        #Key input
        keys = py.key.get_pressed()

        #Movement force based on WASD keys pressed
        movement_vector = Vec2(0,0)
        if flock.stunned == False:
            if keys[py.K_w]:
                movement_vector.y -= 1
            if keys[py.K_s]:
                movement_vector.y += 1
            if keys[py.K_a]:
                movement_vector.x -= 1
            if keys[py.K_d]:
                movement_vector.x += 1
        
        for e in py.event.get():
            if e.type == py.QUIT: 
                game = False
                sys.exit()

            #Get user input
            if e.type == py.MOUSEBUTTONDOWN:
                mouse_pos = py.mouse.get_pos()
                flock.num_boids = len(boids)
                if len(boids) > 0:
                    random_boid_ind = random.randint(0,len(boids)-1)
                    flock.LaunchDuckling(mouse_pos - boids[random_boid_ind].pos, 10, boids[random_boid_ind])
                    removed_boid = boids.pop(random_boid_ind)
                    removed_boids.append(removed_boid)

            if e.type == py.KEYDOWN:
                key = e.key
                if key == py.K_SPACE:
                    flock.Dash(Vec2(np.cos(np.arctan2(flock.vel.y, flock.vel.x)), np.sin(np.arctan2(flock.vel.y, flock.vel.x))) * 50) # player dashes in the direction they are moving/looking
            if e.type == py.KEYUP:
                key = e.key

        flock.Movement(movement_vector)

        # -- DRAW --
        window.fill(DARKGRAY)

        rounded_flock_vel = Vec2(round(flock.vel.x), round(flock.vel.y))

        seen_rects = []
        for bg in map:
            bg.x -= rounded_flock_vel.x
            bg.y -= rounded_flock_vel.y

            if bg.x + bg.w >= 0 and bg.y + bg.h >= 0: #only render the backgrounds on screen to save performance
                py.draw.rect(window, CYAN, bg)
                seen_rects.append(bg)

        active_cols = []
        for col in colliders:
            col.x -= rounded_flock_vel.x
            col.y -= rounded_flock_vel.y

            if debug_colliders and (col.x + col.w >= 0 and col.y + col.h >= 0): #only render the colliders on screen to save performance
                py.draw.rect(window, RED, col, 10)
                active_cols.append(col)

        enemy_rects = []
        removed_enemies = []
        for enemy in enemies:
            enemy.AddForce(SetMagnitude(LimitMagnitude(flock.pos - enemy.pos, 5),5))
            enemy.CheckCollisions(active_cols)
            enemy.Update(flock)
            if enemy.despawn_timer <= 0:
                    removed_enemies.append(enemy)
            enemy.Draw(window)
            enemy_rects.append(enemy.rect)

        for enemy in removed_enemies:
            enemies.remove(enemy)

        for boid in boids:
            #Add forces to boid
            if Normalize(flock.screen_pos - boid.pos) < flock.range:
                boid.max_speed = 5
                boid.alignment_enabled = False
            else:
                boid.max_speed = 6
                boid.alignment_enabled = True
                
            boid.Flock(boids, flock=flock, flock_params=flock_params)

            #Update Boid
            boid.Update(flock)

            #Draw Boid
            #direction_ray = Ray(boid.pos, SetMagnitude(LimitMagnitude(boid.vel,5),5), 15)
            #direction_ray.DebugDraw(window)
            boid.Draw(window)

        for boid in removed_boids:
            boid_col_enemy_index = boid.CheckCollisions(enemy_rects)
            if boid_col_enemy_index != -1:
                enemies[boid_col_enemy_index].health -= flock.boid_damage
                if enemies[boid_col_enemy_index].health <= 0:
                    enemies.remove(enemies[boid_col_enemy_index])
                removed_boids.remove(boid)
            boid.Update(flock)
            boid.Draw(window)

        flock.AddForce(movement_vector * flock.max_speed)
        
        # COLLISIONS
        flock.CheckWallCollisions(active_cols)
        flock.Update()
        flock.Draw(window)

        # Draw text
        window.blit(fps_text, (200, 50))
        window.blit(flock_boid_num_text, (200, 100))
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
        
        boid = Boid(pos, vel, accel, blue_arrow_img, bound_to_window=True)
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
                    
                    boid = Boid(pos, vel, accel, blue_arrow_img, bound_to_window=False)
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