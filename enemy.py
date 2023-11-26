import pygame, sys
import random

# Inicializar pygame
pygame.init()

WIDTH = 800
HEIGHT = 800
ENEMY_SIZE = 40
ENEMY_SPEED = 2
ENEMY_VISION_RANGE = 100
ENEMY_INCREMENT_SPEED = 0.1
ENEMY_COLOR = (255, 0, 0)
VISION_RANGE = 150  # Rango de vision del enemigo

# Configurar la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Automaton Runner')

# Clase para el enemigo con autómata finito
class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.dx = ENEMY_SPEED
        self.dy = 0
        self.state = "patrolling"

    def move(self, player):
        if player.powered_up:
            # Lógica para alejarse del jugador
            if self.x < player.x:
                self.dx = -ENEMY_SPEED
            else:
                self.dx = ENEMY_SPEED
            if self.y < player.y:
                self.dy = -ENEMY_SPEED
            else:
                self.dy = ENEMY_SPEED
        else:
            if self.state == "patrolling":
                self.x += self.dx
                self.y += self.dy
                if self.x < 0 or self.x > WIDTH - ENEMY_SIZE:
                    self.dx = -self.dx
                if self.y < 0 or self.y > HEIGHT - ENEMY_SIZE:
                    self.dy = -self.dy
                # Cambiar a estado de persecución si el jugador está cerca
                if abs(self.x - player.x) < 100 and abs(self.y - player.y) < 100:
                    self.state = "chasing"
                    
            elif self.state == "chasing":
                # Cambiar a estado de patrullaje si el jugador está lejos
                if abs(self.x - player.x) > VISION_RANGE or abs(self.y - player.y) > VISION_RANGE:
                    self.state = "patrolling"
                    return
                
                if self.x < player.x:
                    self.dx = min(ENEMY_SPEED, player.x - self.x)
                else:
                    self.dx = -min(ENEMY_SPEED, self.x - player.x)
                
                if self.y < player.y:
                    self.dy = min(ENEMY_SPEED, player.y - self.y)
                else:
                    self.dy = -min(ENEMY_SPEED, self.y - player.y)
                
                self.x += self.dx
                self.y += self.dy


    def draw(self, screen):
        pygame.draw.rect(screen, ENEMY_COLOR, (self.x, self.y, ENEMY_SIZE, ENEMY_SIZE))


    def draw(self, screen):
        pygame.draw.rect(screen, ENEMY_COLOR, (self.x, self.y, ENEMY_SIZE, ENEMY_SIZE))
