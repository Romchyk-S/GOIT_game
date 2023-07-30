# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 16:23:50 2023

@author: romas
"""

import pygame

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
        