# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 16:27:28 2023

@author: romas
"""

import pygame

def create_surface(main_display: pygame.surface.Surface, size: tuple[int], color: tuple[int], coordinates: tuple[int]):
        
    new = pygame.Surface(size)
    
    new.fill(color)
    
    new_rect = pygame.Rect(*coordinates, *size)
    
    main_display.blit(new, new_rect)
    
    pygame.display.flip()
    
    return new, new_rect
