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
PLATFORM_HEIGHT = 20
PLATFORM_WIDTH = 150
PLAYER_COLOR = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Automaton Runner')


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
            # PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 250), 
            #                 text_input="PLAY", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
            #platform=pygame.image.load(("assets/plataformas.png")
            #pygame.Rect(platform[0], platform[1]
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
