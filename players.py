import pygame, sys
import random

# Inicializar pygame
pygame.init()

# Constantes
WIDTH = 800
HEIGHT = 800
PLAYER_SIZE = 50
PLAYER_SPEED = 5
PLAYER_JUMP = 100
JUMP_STRENGTH = -15
GRAVITY = 1
ENEMY_SIZE = 40
ENEMY_SPEED = 2
PLATFORM_HEIGHT = 20
PLATFORM_WIDTH = 150
VISION_RANGE = 150  # Rango de vision del enemigo
POWERUP_SIZE = 30
POWERUP_COLOR = (255, 255, 0)  # Amarillo, como en Pac-Man


# Configurar la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Automaton Runner')

background_image = pygame.image.load("square/fondo_b.png")


# Clases del juego

# Clase para el jugador
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - PLAYER_SIZE - 10
        self.dx = 0
        self.dy = 0
        self.jumping = False
        self.on_ground = True
        self.times_hit = 0
        self.powered_up = False
        self.powerup_start_time = 0
        self.collected_powerup = False

    def activate_powerup(self):
        self.powered_up = True
        self.powerup_start_time = pygame.time.get_ticks()
        self.collected_powerup = True
    
    def deactivate_powerup(self):
        self.powered_up = False
    
    def check_powerup_duration(self):
        if self.powered_up and pygame.time.get_ticks() - self.powerup_start_time > POWERUP_DURATION:
            self.deactivate_powerup()

    def move(self, platforms):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.dx = -PLAYER_SPEED
        elif keys[pygame.K_RIGHT]:
            self.dx = PLAYER_SPEED
        else:
            self.dx = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.dy = JUMP_STRENGTH
            self.jumping = True
            self.on_ground = False

        # Aplicar gravedad
        self.dy += GRAVITY

        # Colisiones con plataformas
        for platform in platforms:
            platform_rect = pygame.Rect(platform[0], platform[1], PLATFORM_WIDTH, PLATFORM_HEIGHT)
            if platform_rect.colliderect(self.x, self.y + self.dy, PLAYER_SIZE, PLAYER_SIZE):
                if self.dy > 0:  # Si está cayendo
                    self.dy = 0
                    self.y = platform[1] - PLAYER_SIZE
                    self.on_ground = True
                    self.jumping = False

        self.x += self.dx
        self.y += self.dy

        # Mantener al jugador dentro de la ventana y en el suelo
        self.x = max(0, min(WIDTH - PLAYER_SIZE, self.x))
        if self.y > HEIGHT - PLAYER_SIZE:
            self.y = HEIGHT - PLAYER_SIZE
            self.dy = 0
            self.on_ground = True
            self.jumping = False

    def draw(self, screen):
        if self.powered_up:
            color = (0, 0, 255)  # Color azul cuando está en modo powered up
        else:
            color = PLAYER_COLOR
        pygame.draw.rect(screen, color, (self.x, self.y, PLAYER_SIZE, PLAYER_SIZE))

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

class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = POWERUP_SIZE

    def draw(self, screen):
        pygame.draw.circle(screen, POWERUP_COLOR, (self.x + self.size // 2, self.y + self.size // 2), self.size // 2)
