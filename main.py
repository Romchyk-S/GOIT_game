# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 13:36:50 2023

@author: romas
"""

import pygame

import random

import os

print()

animation_pics_dir = 'Бандерогусак для анімації (goose)'

goose_pics = os.listdir(animation_pics_dir)

def create_surface(main_display: pygame.surface.Surface, size: tuple[int], color: tuple[int], coordinates: tuple[int]):
        
    new = pygame.Surface(size)
    
    new.fill(color)
    
    new_rect = pygame.Rect(*coordinates, *size)
    
    main_display.blit(new, new_rect)
    
    pygame.display.flip()
    
    return new, new_rect


def check_keys(key: pygame.key.ScancodeWrapper, movements: dict[bool], skip_next: bool, curr_speed: list[int], player_speed_num: int) -> tuple:
    
    if skip_next:
        
        skip_next = False
        
    else:
        
        if movements.get('down') and movements.get('right'):
            
            curr_speed = [player_speed_num, player_speed_num]
            
            skip_next = True
            
        elif movements.get('down') and movements.get('left'):
             
            curr_speed = [-player_speed_num, player_speed_num]
            
            skip_next = True
            
        elif (movements.get('down') and movements.get('up')) or (movements.get('right') and movements.get('left')):
            
            curr_speed = [0, 0]
            
            skip_next = True
            
        elif movements.get('up') and movements.get('right'):
            
            curr_speed = [player_speed_num, -player_speed_num]
            
            skip_next = True
            
        elif movements.get('up') and movements.get('left'):
             
            curr_speed = [-player_speed_num, -player_speed_num]
            
            skip_next = True
        
        elif movements.get('down'):
       
            curr_speed = [0, player_speed_num]
            
        elif movements.get('right'):
            
            curr_speed = [player_speed_num, 0]
            
        elif movements.get('left'):
        
            curr_speed = [-player_speed_num, 0]
            
        elif movements.get('up'):
        
            curr_speed = [0, -player_speed_num]
    
    return curr_speed, skip_next

def check_borders(player_rect: pygame.rect.Rect, window_size: tuple, speed: list[int]) -> list[int]:

    if player_rect.bottom >= window_size[1] or player_rect.top < 0:
    
        speed[1] = -speed[1]
        
    if player_rect.left < 0 or player_rect.right >= window_size[0]:
        
        speed[0] = -speed[0]
        
    return speed
        


# first width, then height
window_size = 1200, 800

# first width, then height
player_size = 182, 76

# RGB
player_color = 255, 255, 255

# x, y
player_coordinates = 0, window_size[1]/2

enemy_size = 102, 36

enemy_color = 255, 0, 0

bonus_size = 89, 149

bonus_color = 124, 252, 0

black_color = 0, 0, 0

background = pygame.transform.scale(pygame.image.load('background.png'), window_size)

background_x_1 = 0

background_x_2 = background.get_width()

background_move = 3

rocket = pygame.transform.scale(pygame.image.load('enemy.png'), enemy_size)

bonus_img = pygame.transform.scale(pygame.image.load('bonus.png'), bonus_size)

font_size = 20



pygame.init()

font = pygame.font.SysFont('Verdana', font_size)


main_display = pygame.display.set_mode(window_size)

FPS = pygame.time.Clock()

player, player_rect = create_surface(main_display, player_size, player_color, player_coordinates)


playing = True

points = 0

skip_next = False

player_speed_num = 4

player_speed = [0, 0]

enemies, bonuses = [], []

CREATE_ENEMY = pygame.USEREVENT + 1

pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = CREATE_ENEMY + 1

pygame.time.set_timer(CREATE_BONUS, 3000)

CHANGE_GOOSE = CREATE_BONUS + 1

pygame.time.set_timer(CHANGE_GOOSE, 250)

start = pygame.time.get_ticks()

image_index = 0

goose = pygame.transform.scale(pygame.image.load(f'{animation_pics_dir}'+f'\{goose_pics[image_index]}').convert_alpha(), player_size)

while playing:
    
    FPS.tick(120)
    
    for event in pygame.event.get():
        
        key = pygame.key.get_pressed()

        if event.type == pygame.QUIT:
            
            playing = False
            
        if event.type == CREATE_ENEMY:
            
            # x, y
            enemy_coordinates = window_size[0], random.randint(int(window_size[1]*0.1), int(window_size[1]*0.95))
            
            new_enemy = list(create_surface(main_display, enemy_size, enemy_color, enemy_coordinates))
            
            new_enemy.append([random.randint(-8, -4), 0])
            
            enemies.append(new_enemy)
            
        if event.type == CREATE_BONUS:
            
            # x, y
            bonus_coordinates = random.randint(window_size[0]*0.6, window_size[0]), 0
            
            new_bonus = list(create_surface(main_display, bonus_size, bonus_color, bonus_coordinates))
            
            new_bonus.append([0, random.randint(4, 8)])
            
            bonuses.append(new_bonus)
            
        if event.type == CHANGE_GOOSE:
            
            try:
            
                goose = pygame.transform.scale(pygame.image.load(f'{animation_pics_dir}'+f'\{goose_pics[image_index]}').convert_alpha(), player_size)
                
            except IndexError:
                
                image_index = 0
                
                goose = pygame.transform.scale(pygame.image.load(f'{animation_pics_dir}'+f'\{goose_pics[image_index]}'), player_size)
                
            image_index += 1
            
            
        if True in key:
            
            movements = {'down': key[pygame.K_DOWN] or key[pygame.K_s], 'left': key[pygame.K_LEFT] or key[pygame.K_a], 
                         'right': key[pygame.K_RIGHT] or key[pygame.K_d], 'up': key[pygame.K_UP] or key[pygame.K_w]}
            
            player_speed, skip_next = check_keys(key, movements, skip_next, player_speed, player_speed_num)
            
    player_speed = check_borders(player_rect, window_size, player_speed)
    
    background_x_1 -= background_move
    
    background_x_2 -= background_move
    
    if background_x_1 < -background.get_width():
        
        background_x_1 = background.get_width()
        
    if background_x_2 < -background.get_width():
        
        background_x_2 = background.get_width()
    
    main_display.blit(background, (background_x_1, 0))
    
    main_display.blit(background, (background_x_2, 0))
    
    main_display.blit(goose, player_rect)   
    
         
    player_rect = player_rect.move(player_speed)
    
    for enemy in enemies:
        
        enemy_surf, enemy_rect, enemy_speed = enemy
         
        enemy_rect = enemy_rect.move(enemy_speed)
        
        main_display.blit(rocket, enemy_rect)
        
        enemy[1] = enemy_rect
        
        if player_rect.colliderect(enemy[1]):
            
            playing = False
        
        if enemy[1].left < 0:
            
            enemies.pop(enemies.index(enemy))
            
    for bonus in bonuses:
        
         bonus_surf, bonus_rect, bonus_speed = bonus
          
         bonus_rect = bonus_rect.move(bonus_speed)
         
         main_display.blit(bonus_img, bonus_rect)
         
         bonus[1] = bonus_rect
         
         if player_rect.colliderect(bonus[1]):
             
             bonuses.pop(bonuses.index(bonus))
             
             points += 1
         
         if bonus[1].bottom > window_size[1]:
             
             bonuses.pop(bonuses.index(bonus))
             
    time_played = round((pygame.time.get_ticks()-start)*10**(-3), 3)
             
    main_display.blit(font.render(f"Points: {points}", True, black_color), (window_size[0]-100, font_size))
    
    main_display.blit(font.render(f"Enemies: {len(enemies)}", True, black_color), (window_size[0]-250, font_size))
    
    main_display.blit(font.render(f"Bonuses: {len(bonuses)}", True, black_color), (window_size[0]-400, font_size))
    
    main_display.blit(font.render(f"Time played (s): {time_played}", True, black_color), (window_size[0]-700, font_size))
    
    pygame.display.flip()

print("GAME OVER")

print(f"Points: {points}")