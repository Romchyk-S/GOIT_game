# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 13:36:50 2023

@author: romas
"""

import pygame


def check_borders(player_rect: pygame.rect.Rect, window_size: tuple) -> None|list[int]:

    if player_rect.bottom >= window_size[1]:
    
        speed = [1, -1]
        
    elif player_rect.left < 0:
        
        speed = [1, 1]
        
    elif player_rect.right >= window_size[0]:
        
        speed = [-1, -1]
        
    elif player_rect.top < 0:
        
        speed = [-1, 1]
        
    try:
        
        return speed
        
    except UnboundLocalError:
        
        return None

# first width, then height
window_size = 1200, 800

# first width, then height
player_size = 20, 20

# RGB
player_color = 255, 255, 255

pygame.init()


main_display = pygame.display.set_mode(window_size)

FPS = pygame.time.Clock()


player = pygame.Surface(player_size)

player.fill(player_color)

player_rect = player.get_rect()

main_display.blit(player, player_rect)

pygame.display.flip()


playing = True

curr_speed = [0, 0]

while playing:
    
    FPS.tick(120)
    
    for event in pygame.event.get():
        
        key = pygame.key.get_pressed()

        if event.type == pygame.QUIT:
            
            playing = False
            
        if True in key:
        
            if key[pygame.K_DOWN] or key[pygame.K_s]:
                
                curr_speed = [0, 1]
                
            elif key[pygame.K_RIGHT] or key[pygame.K_d]:
                
                curr_speed = [1, 0]
                
            elif key[pygame.K_LEFT] or key[pygame.K_a]:
            
                curr_speed = [-1, 0]
                
            elif key[pygame.K_UP] or key[pygame.K_w]:
            
                curr_speed = [0, -1]
            
    curr_speed_new = check_borders(player_rect, window_size)
        
    if curr_speed_new != None:
        
        curr_speed = curr_speed_new
            
    main_display.fill((0,0,0))
    
    main_display.blit(player, player_rect)   
         
    player_rect = player_rect.move(curr_speed)
    
    pygame.display.flip()