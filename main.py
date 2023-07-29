# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 13:36:50 2023

@author: romas
"""

import pygame

import random


def create_surface(main_display: pygame.surface.Surface, size: tuple[int], color: tuple[int], coordinates: tuple[int]):
        
    new = pygame.Surface(size)
    
    new.fill(color)
    
    new_rect = pygame.Rect(*coordinates, *size)
    
    main_display.blit(new, new_rect)
    
    pygame.display.flip()
    
    return new, new_rect


def check_keys(key: pygame.key.ScancodeWrapper, movements: dict[bool], skip_next: bool, curr_speed: list[int]) -> tuple:
    
    if skip_next:
        
        skip_next = False
        
    else:
        
        if movements.get('down') and movements.get('right'):
            
            curr_speed = [1, 1]
            
            skip_next = True
            
        elif movements.get('down') and movements.get('left'):
             
            curr_speed = [-1, 1]
            
            skip_next = True
            
        elif (movements.get('down') and movements.get('up')) or (movements.get('right') and movements.get('left')):
            
            curr_speed = [0, 0]
            
            skip_next = True
            
        elif movements.get('up') and movements.get('right'):
            
            curr_speed = [1, -1]
            
            skip_next = True
            
        elif movements.get('up') and movements.get('left'):
             
            curr_speed = [-1, -1]
            
            skip_next = True
        
        elif movements.get('down'):
       
            curr_speed = [0, 1]
            
        elif movements.get('right'):
            
            curr_speed = [1, 0]
            
        elif movements.get('left'):
        
            curr_speed = [-1, 0]
            
        elif movements.get('up'):
        
            curr_speed = [0, -1]
    
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
player_size = 20, 20

# RGB
player_color = 255, 255, 255

# x, y
player_coordinates = 0, 0

enemy_size = 30, 30

enemy_color = 255, 0, 0

bonus_size = 20, 20

bonus_color = 124, 252, 0


pygame.init()


main_display = pygame.display.set_mode(window_size)

FPS = pygame.time.Clock()

player, player_rect = create_surface(main_display, player_size, player_color, player_coordinates)


playing = True

skip_next = False

player_speed = [0, 0]

enemies = []

bonuses = []

CREATE_ENEMY = pygame.USEREVENT + 1

pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = CREATE_ENEMY + 1

pygame.time.set_timer(CREATE_BONUS, 5000)



while playing:
    
    FPS.tick(120)
    
    for event in pygame.event.get():
        
        key = pygame.key.get_pressed()

        if event.type == pygame.QUIT:
            
            playing = False
            
        if event.type == CREATE_ENEMY:
            
            # x, y
            enemy_coordinates = window_size[0], random.randint(0, window_size[1])
            
            new_enemy = list(create_surface(main_display, enemy_size, enemy_color, enemy_coordinates))
            
            new_enemy.append([random.randint(-6, -1), 0])
            
            enemies.append(new_enemy)
            
        if event.type == CREATE_BONUS:
            
            # x, y
            bonus_coordinates = random.randint(0, window_size[0]), 0
            
            new_bonus = list(create_surface(main_display, bonus_size, bonus_color, bonus_coordinates))
            
            new_bonus.append([0, random.randint(1, 6)])
            
            bonuses.append(new_bonus)
            
        if True in key:
            
            movements = {'down': key[pygame.K_DOWN] or key[pygame.K_s], 'left': key[pygame.K_LEFT] or key[pygame.K_a], 'right': key[pygame.K_RIGHT] or key[pygame.K_d], 'up': key[pygame.K_UP] or key[pygame.K_w]}
            
            player_speed, skip_next = check_keys(key, movements, skip_next, player_speed)
            
    player_speed = check_borders(player_rect, window_size, player_speed)
            
    main_display.fill((0, 0, 0))
    
    main_display.blit(player, player_rect)   
    
         
    player_rect = player_rect.move(player_speed)
    
    for enemy in enemies:
        
        enemy_surf, enemy_rect, enemy_speed = enemy
         
        enemy_rect = enemy_rect.move(enemy_speed)
        
        main_display.blit(enemy_surf, enemy_rect)
        
        enemy[1] = enemy_rect
        
        if enemy[1].left < 0:
            
            enemies.pop(enemies.index(enemy))
            
    for bonus in bonuses:
        
         bonus_surf, bonus_rect, bonus_speed = bonus
          
         bonus_rect = bonus_rect.move(bonus_speed)
         
         main_display.blit(bonus_surf, bonus_rect)
         
         bonus[1] = bonus_rect
         
         if bonus[1].bottom > window_size[1]:
             
             bonuses.pop(bonuses.index(bonus))
    
    pygame.display.flip()