##--- CITATIONS ---
# 1. Reynolds, Craig. “Boids.” Red3d, 1995, www.red3d.com/cwr/boids/. 
# 2. Lague, Sebastian. “Coding Adventure: Boids.” YouTube, 26 Aug. 2019, www.youtube.com/watch?v=bqtqltqcQhw&t=118s. 
# 3. Gavin. “How Do You Detect Where Two Line Segments Intersect?” Stack Overflow, 28 Dec. 2009, stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect. 
# 4. 
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
from ray import *
from helpfunctions import *

py.init()
screen_width, screen_height = 1600, 900
py.display.set_caption("Boids")

menu_flag = True
performance_test_flag = False
game_flag = False

window_flags = py.DOUBLEBUF | py.FULLSCREEN
window = py.display.set_mode((screen_width, screen_height), window_flags, 8)
clock = py.time.Clock()
fps = 60

font_arial20 = py.font.SysFont('Arial', 20)
font_bahnschrift25 = py.font.SysFont('Bahnschrift', 25)
font_bahnschriftsb30 = py.font.SysFont('Bahnschrift', 30)
font_arial30 = py.font.SysFont('Arial', 30)
font_arial80 = py.font.SysFont('Arial', 80)

## MAIN GAME

def MainGame(game):
    time_scale = 1 # used for controlling how fast the speed at which the game updates, useful for freezing the game (pausing or game over)

    # LOAD IN ALL IMAGES (some may not be used)
    circle_15px_img = py.image.load('resources/circle_15px.png').convert_alpha()
    circle_50px_img = py.image.load('resources/circle_50px.png').convert_alpha()
    circle_100px_img = py.image.load('resources/circle_100px.png').convert_alpha()
    blue_arrow_img = py.image.load('resources/blue_arrow.png').convert_alpha()
    yellow_arrow_img = py.image.load('resources/yellow_arrow.png').convert_alpha()
    ducky_small_img = py.image.load('resources/ducky_small.png').convert_alpha()
    ducky_medium_img = py.image.load('resources/ducky_medium.png').convert_alpha()
    ducky_large_img = py.image.load('resources/ducky_large.png').convert_alpha()
    map_img = py.image.load('resources/map.jpg').convert_alpha()

    map = [ # all rects for the map
        py.Rect(-2000, -2000, 4000, 4000),
    ]

    debug_colliders = False # debug option for colliders
    colliders = [ # all rects for colliders
        py.Rect(-2000, -2600, 4000, 1000), # top
        py.Rect(-2000, 1600, 4000, 1000), # bottom
        py.Rect(-2600, -2000, 1000, 4000), # left
        py.Rect(1600, -2000, 1000, 4000), # right
    ]
    
    # offset the map by a certain amount
    map_offset = [1000, 0] 
    for bg in map:
        bg.x += map_offset[0]
        bg.y += map_offset[1]
    for col in colliders:
        col.x += map_offset[0]
        col.y += map_offset[1]

    # flock parameters for flock calculations
    flock_params = FlockParams(separation_distance = 50, alignment_distance = 100, cohesion_distance = 200, separation_factor = 1, alignment_factor = 1, cohesion_factor = 1)

    # boids and removed boids lists
    boids = []
    removed_boids = []

    # initialize main flock
    flock = Flock(Vec2(screen_width/2, screen_height/2), Vec2(0,0), 10, range=200, health=25, img=ducky_large_img)

    # spawn ducklings
    SpawnDucklingsRandom(boids, flock, ducky_small_img)

    # initialize enemies
    enemies = []
    sploder_enemy = EnemyParams("sploder", circle_50px_img, circle_50px_img, circle_50px_img, attack_range=75, speed=4, health=1, damage=5, value=25)
    boss_enemy = EnemyParams("boss", circle_100px_img, circle_100px_img, circle_100px_img, attack_range = 200, speed=1, health=15, damage=20, value=100)

    # initialize waves
    total_waves = 0
    current_wave = 0
    wave_countdown = 300
    waves = [
        (0, sploder_enemy),
        (3, sploder_enemy), (5, sploder_enemy), (3, sploder_enemy), (7, sploder_enemy), (1, boss_enemy),
        (5, sploder_enemy), (2, sploder_enemy), (2, sploder_enemy), (6, sploder_enemy), (1, boss_enemy),
    ]

    # call flock draw function to avoid errors
    flock.Draw(window)
    
    # Spawn first wave
    SpawnWave(enemies, waves[current_wave][0], waves[current_wave][1])

    # UPGRADES
    launch_upgrade = False
    dash_upgrade = False

    # CONTROLS TEXT
    controls_text = font_bahnschriftsb30.render("CONTROLS", True, WHITE)
    launch_duckling_text = font_bahnschrift25.render("[LMB] Launch Duckling", True, WHITE)
    reload_input_text = font_bahnschrift25.render("[R] Recall Ducklings (Must Have 0)", True, WHITE)
    dash_input_text = font_bahnschrift25.render("[SPACE] Dash", True, WHITE)
    menu_text = font_bahnschrift25.render("[M] Menu", True, WHITE)
    quit_text = font_bahnschrift25.render("[ESC] Quit", True, WHITE)

    # OTHER TEXT
    game_over_text = font_arial80.render("GAME OVER", True, WHITE) # render Game Over text in white
    paused_text = font_arial80.render("PAUSED", True, WHITE) # renders paused text
    launch_upgrade_text = font_arial80.render("DUCKLING UPGRADE", True, WHITE) # launch upgrade text
    dash_upgrade_text = font_arial80.render("DASH UPGRADE", True, WHITE) # dash upgrade text

    while game: # main loop
        clock.tick(fps)

        # freeze game if player is dead
        if flock.health <= 0:
            time_scale = 0

        # RENDER TEXT
        fps_text = font_bahnschrift25.render("FPS: " + str(round(clock.get_fps())), True, WHITE) # renders fps text
        wave_text = font_bahnschrift25.render("Wave: " + str(total_waves), True, WHITE) # renders current wave text
        flock_health_text = font_bahnschrift25.render("Health: " + str(flock.health), True, WHITE) # renders health text
        flock_num_coins_text = font_bahnschrift25.render("Coins: " + str(flock.coins), True, WHITE) # renders num coins text

        flock.num_boids = len(boids)
        flock_boid_num_text = font_bahnschrift25.render("Ducklings: " + str(flock.num_boids), True, WHITE) # renders num ducklings text

        # WAVE COUNTDOWN TEXT
        if len(enemies) == 0: # check if enemies in current wave are defeated
            launch_upgrade = False
            dash_upgrade = False
            if current_wave == 4: # current wave is 4
                launch_upgrade = True
                flock.launch_cooldown -= 3 # increase "fire rate"
            if current_wave == 9: # current wave is 9
                dash_upgrade = True
                flock.dash_cooldown -= 3 # decrease dash cooldown

            wave_countdown -= 1 * time_scale # start counting down each frame (millisecond)
            wave_countdown_text = font_arial80.render(str(round(wave_countdown / 60)), True, WHITE) # render the text in seconds, and round it
            if wave_countdown <= 0: # check if countdown is over
                current_wave += 1 # increment wave
                total_waves += 1 # increase total waves
                if (current_wave > len(waves) - 1): # check if current wave is out of range of the waves list
                    current_wave = 0 # loop current wave back around to beginning
                SpawnWave(enemies, waves[current_wave][0], waves[current_wave][1]) # spawn a new wave of enemies based on the waves list
                wave_countdown = 300 # reset the countdown for next wave

        # Key input
        keys = py.key.get_pressed() # gets the keys pressed

        # Movement force based on WASD keys pressed
        movement_vector = Vec2(0,0) # reset movement vector to get movement each frame
        if flock.stunned == False: # player can move
            if keys[py.K_w]: # w key pressed
                movement_vector.y -= 1 # move up
            if keys[py.K_s]: # s key pressed
                movement_vector.y += 1 # move down
            if keys[py.K_a]: # a key pressed  
                movement_vector.x -= 1 # move left
            if keys[py.K_d]: # d key pressed 
                movement_vector.x += 1 # move right
        
        for e in py.event.get(): # get events
            if e.type == py.QUIT or (e.type == py.KEYDOWN and e.key == py.K_ESCAPE): # quit event
                game = False # game boolean false
                sys.exit() # exit game

            #Get user input
            if e.type == py.MOUSEBUTTONDOWN: # left mouse button down
                mouse_pos = py.mouse.get_pos() # get mouse position
                if len(boids) > 0 and time_scale > 0: # check if there are boids
                    random_boid_ind = random.randint(0,len(boids)-1) # get a random boid
                    flock.LaunchDuckling(mouse_pos - boids[random_boid_ind].pos, 10, boids[random_boid_ind]) # launch that random boid in the direction of the mouse
                    removed_boid = boids.pop(random_boid_ind) # remove the boid from boids list
                    removed_boids.append(removed_boid) # append the boid to removed boids list

            if e.type == py.KEYDOWN: # key down
                key = e.key # get key 
                if key == py.K_SPACE: # check key is space
                    flock.Dash(Vec2(np.cos(np.arctan2(flock.vel.y, flock.vel.x)), np.sin(np.arctan2(flock.vel.y, flock.vel.x))) * 50) # player dashes in the direction they are moving/looking
                if key == py.K_r: # check key is r
                    if flock.num_boids <= 0: # check num boids less than or equal to 0
                        SpawnDucklingsRandom(boids, flock, ducky_small_img) # "reload" ducklings
                if key == py.K_TAB and flock.health > 0: # check key is tab
                    if time_scale == 1: time_scale = 0 # pause game
                    elif time_scale == 0: time_scale = 1 # unpause game
                if key == py.K_m: # check key is m
                    Menu(True, False, False) # go back to menu
                    
            if e.type == py.KEYUP: # key up
                key = e.key # get key

        flock.Movement(movement_vector) # move flock based on movement vector

        # -- DRAW --
        window.fill((50, 137, 44)) # fill window with color

        rounded_flock_vel = Vec2(round(flock.vel.x), round(flock.vel.y)) * time_scale # round flock velocity for smooth object movement

        for bg in map: # get all backgrounds, this was more relevant when I had a whole map going on, but I decided it would be best if I focused on other aspects of the game
            bg.x -= rounded_flock_vel.x # move background position based on flock movement
            bg.y -= rounded_flock_vel.y # move background position based on flock movement

            if bg.x + bg.w >= 0 and bg.y + bg.h >= 0: # only render the backgrounds on screen to save performance
                window.blit(map_img, (bg.x, bg.y)) # draw background
        

        active_cols = [] # list for only the active colliders so we don't test them all if we don't need to
        for col in colliders: # loop through colliders
            col.x -= rounded_flock_vel.x # move background position based on flock movement
            col.y -= rounded_flock_vel.y # move background position based on flock movement

            if col.x + col.w >= 0 and col.y + col.h >= 0: # only use the colliders on screen to save performance
                active_cols.append(col) # append to active collider list
                if debug_colliders: # check if debugging
                    py.draw.rect(window, RED, col, 10) # draw debug collider rects

        enemy_rects = [] # enemy rects
        removed_enemies = [] # enemies to be removed
        for enemy in enemies: # loop through enemies
            enemy.Separate(enemies) # separate enemies from eachother
            enemy.CheckCollisions(active_cols) # check enemy collisions with walls
            enemy.Update(time_scale, flock) # update enemy physics and positions

            if enemy.despawn_timer <= 0: # check if enemy is dead
                removed_enemies.append(enemy) # add to remove list
            
            if enemy.can_damage: # check if enemy can damage
                enemy_rects.append(enemy.rect) # append to rect list. If an enemy is able to damage then it should be tested
            enemy.Draw(window) # draw enemy

        for enemy in removed_enemies: # loop through removed enemies
            if len(enemies) > 0: enemies.remove(enemy) # remove enemy from array

        for boid in boids: # loop through boids
            #Add forces to boid
            if Normalize(flock.pos - boid.pos) < flock.range: # check if boid is near flock
                boid.max_speed = 6 # make boid max speed normal
                boid.alignment_enabled = False # disable alignment
            else: # boid away from flock
                boid.max_speed = 8 # speed up boid to catch up with flock
                boid.alignment_enabled = True # enable alignment
                
            boid.Flock(boids, flock=flock, flock_params=flock_params) # perform flocking calculations

            #Update Boid
            boid.Update(time_scale, flock)

            #Draw Boid
            #direction_ray = Ray(boid.pos, SetMagnitude(LimitMagnitude(boid.vel,5),5), 15)
            #direction_ray.DebugDraw(window)
            boid.Draw(window)

        for boid in removed_boids: # loop through removed boids
            boid_col_enemy_index = boid.CheckCollisions(enemy_rects) # get collision index
            if boid_col_enemy_index != -1: # check if there is a collision
                enemies[boid_col_enemy_index].health -= flock.boid_damage # decrease enemy health
                if enemies[boid_col_enemy_index].health <= 0: # make sure enemy has no more health
                    flock.health += 1 # increase health for each enemy killed
                    flock.coins += enemies[boid_col_enemy_index].value # add coins based on value of enemy
                    enemies.remove(enemies[boid_col_enemy_index]) # remove enemy from list 
                removed_boids.remove(boid) # remove boid from list
            boid.Update(time_scale, flock) # update boid
            if boid.pos.x > 1600 or boid.pos.x < -boid.img.get_width() or boid.pos.y > 900 or boid.pos.y < -boid.img.get_height(): # check if boid is offscreen
                removed_boids.remove(boid) # remove boid from list

            boid.Draw(window) # draw boid

        flock.AddForce(movement_vector * flock.max_speed) # add movement force to flock
        
        # COLLISIONS
        flock.CheckWallCollisions(active_cols) # check flock collision with walls
        if len(enemy_rects) > 0: # check has enemies
            flock_col_enemy = flock.CheckCollisions(enemy_rects) # check flock collision with enemies
            if flock_col_enemy != -1: # has collision
                if enemies[flock_col_enemy] in enemies: # make sure enemy still in enemies
                    if enemies[flock_col_enemy].can_damage and flock.health > 0: # enemy can damage and flock still alive
                        enemies[flock_col_enemy].can_damage = False # enemy can no longer damage
                        flock.health -= enemies[flock_col_enemy].damage # damage flock
                        if flock.health <= 0: # flock health at dead level
                            flock.health = 0 # flock dead
        
        # UPDATE AND DRAW
        flock.Update(time_scale)
        flock.Draw(window)

        # DRAW TEXT ---
        window.blit(fps_text, (100, 50))
        window.blit(wave_text, (100, 80))
        window.blit(flock_health_text, (100, 110))
        window.blit(flock_boid_num_text, (100, 140))
        window.blit(flock_num_coins_text, (100,170))
        window.blit(controls_text, (100, 660))
        window.blit(launch_duckling_text, (100, 700))
        window.blit(reload_input_text, (100, 730))
        window.blit(dash_input_text, (100, 760))
        window.blit(menu_text, (100, 790))
        window.blit(quit_text, (100, 820))
        if wave_countdown < 300: # wave countdown is happening
            window.blit(wave_countdown_text, (screen_width/2, 100))
            if launch_upgrade:
                window.blit(launch_upgrade_text, (screen_width/2 - 200, screen_height/2 - 40))
            if dash_upgrade:
                window.blit(dash_upgrade_text, (screen_width/2 - 150, screen_height/2 - 40))

        if time_scale == 0: # paused or game over
            if flock.health > 0:
                window.blit(paused_text, (screen_width/2 - 125, screen_height/2 - 40))
            else:
                window.blit(game_over_text, (screen_width/2 - 200, screen_height/2 - 40))

        # UPDATE DISPLAY
        py.display.update()



### MENU FUNCTION
def Menu(menu, game, performance_test):
    play_button = py.Rect(screen_width/2 - 100, screen_height/2 - 100, 200, 50)
    play_text = font_arial30.render("GAME", True, WHITE)

    test_button = py.Rect(screen_width/2 - 100, screen_height/2, 200, 50)
    test_text = font_arial30.render("SIMULATION", True, WHITE)

    exit_button = py.Rect(screen_width/2 - 100, screen_height/2 + 100, 200, 50)
    exit_text = font_arial30.render("EXIT", True, WHITE)

    while menu:
        clock.tick(fps)
        window.fill(WHITE)

        for e in py.event.get():
            if e.type == py.QUIT or (e.type == py.KEYDOWN and e.key == py.K_ESCAPE): 
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

        py.draw.rect(window, CYAN, play_button)
        py.draw.rect(window, CYAN, test_button)
        py.draw.rect(window, CYAN, exit_button)
        window.blit(play_text, (play_button.x + 60, play_button.y + 5))
        window.blit(test_text, (test_button.x + 30, test_button.y + 5))
        window.blit(exit_text, (exit_button.x + 70, exit_button.y + 5))

        py.display.update()


### PERFORMANCE TEST FUNCTION
def PerformanceTest(performance_test):
    blue_arrow_img = py.image.load('resources/blue_arrow.png').convert_alpha()

    add_boid_text = font_arial30.render("[T] Add Boid", True, WHITE)
    debug_text = font_arial30.render("[N] Debug Boids", True, WHITE)
    menu_text = font_arial30.render("[M] Return to Menu", True, WHITE)
    quit_text = font_arial30.render("[ESC] Quit", True, WHITE)

    boid_count = 0
    
    flock_params = FlockParams(50, 100, 200, 1, 1, 1)

    debug_boids = False

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

    while performance_test:
        clock.tick(fps)
        fps_text = font_arial30.render("FPS: " + str(round(clock.get_fps())), True, WHITE)
        boid_count_text = font_arial30.render("BOIDS: " + str(boid_count), True, WHITE)

        for e in py.event.get():
            if e.type == py.QUIT or (e.type == py.KEYDOWN and e.key == py.K_ESCAPE): 
                performance_test = False
                sys.exit()
            
            if e.type == py.KEYDOWN:
                if e.key == py.K_t:
                    pos = Vec2(random.randint(0,screen_width), random.randint(0,screen_height))
                    vel = Vec2(random.uniform(-1,1), random.uniform(-1,1))
                    accel = Vec2(1,1)
                    
                    boid = Boid(pos, vel, accel, blue_arrow_img, bound_to_window=True)
                    sections[boid.section[0]][boid.section[1]][(boid.id)] = boid
                    boid_count +=1 
                if e.key == py.K_n: # check key is n
                    debug_boids = not debug_boids # set debug boids to the opposite of what it is
                if e.key == py.K_m: # check key is m
                    Menu(True, False, False) # go back to menu

        window.fill(DARKGRAY) # fill window with color
        
        for x in sections.keys():
            for y in sections[x].keys():
                for boid in sections[x][y].values():
                    #Add forces to boid
                    boid.Flock(sections[x][y], flock_params = flock_params)
                    #Update
                    boid.Update(1)
                    sections = boid.UpdateSections(sections)
                    #Draw
                    if debug_boids:
                        direction_ray = Ray(boid.pos, boid.vel, 15)
                        direction_ray.DebugDraw(window)
                    boid.Draw(window)

        # Draw text
        window.blit(fps_text, (100, 50))
        window.blit(boid_count_text, (100, 100))
        window.blit(add_boid_text, (100, 150))
        window.blit(debug_text, (100, 200))
        window.blit(menu_text, (100, 250))
        window.blit(quit_text, (100, 300))
        py.display.update()



## call functions to run game
Menu(menu_flag, game_flag, performance_test_flag)
py.quit()