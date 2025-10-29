#segunda entrega pops
import pygame
from pygame.locals import *
import sys

# Inicializar Pygame

while True:
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Segunda Entrega POPS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)