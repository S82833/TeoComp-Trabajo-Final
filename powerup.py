import pygame, sys
import random

POWERUP_SIZE = 30
POWERUP_COLOR = (255, 255, 0)  # Amarillo, como en Pac-Man


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Automaton Runner')
#
#class Player:
#
#class Enemy:
#
#
class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = POWERUP_SIZE

    def draw(self, screen):
        pygame.draw.circle(screen, POWERUP_COLOR, (self.x + self.size // 2, self.y + self.size // 2), self.size // 2)
