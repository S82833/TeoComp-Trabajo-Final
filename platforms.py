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
POWERUP_SIZE = 30
PLATFORM_WIDTH = 150

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Automaton Runner')

background_image = pygame.image.load("square/fondo_b.png")

def place_powerup_on_platform(platforms):
    platform = random.choice(platforms[1:-1])
    x = random.randint(platform[0], platform[0] + PLATFORM_WIDTH - POWERUP_SIZE)
    y = platform[1] - POWERUP_SIZE
    return PowerUp(x, y)

# Función para generar plataformas sin superposición vertical y con espacios saltables
def generate_platforms():
    platforms = []

    # Separación mínima horizontal entre plataformas
    MIN_HORIZONTAL_DISTANCE = WIDTH // 3

    # Distancia horizontal máxima que el jugador puede recorrer mientras salta
    calculated_max_distance = int(PLAYER_SPEED * (2 * abs(JUMP_STRENGTH) / GRAVITY) ** 0.5)
    MAX_HORIZONTAL_DISTANCE = max(calculated_max_distance, MIN_HORIZONTAL_DISTANCE)

    # Separación promedio entre plataformas
    AVERAGE_VERTICAL_DISTANCE = 1.5 * PLAYER_JUMP

    # Cantidad fija de plataformas
    NUM_PLATFORMS = int(HEIGHT / AVERAGE_VERTICAL_DISTANCE)

    # Iniciar con una plataforma cerca del suelo en una posición aleatoria del eje x
    y = HEIGHT - PLAYER_JUMP
    x = random.randint(0, WIDTH - PLATFORM_WIDTH)
    platforms.append((x, y))

    for _ in range(NUM_PLATFORMS):
        # La posición y de la siguiente plataforma estará dentro del rango de salto del jugador
        y -= random.randint(PLAYER_JUMP, int(1.5 * PLAYER_JUMP))

        # Decide aleatoriamente si la plataforma estará a la izquierda o a la derecha del anterior
        direction = random.choice([-1, 1])
        
        # Asegura una separación mínima horizontal
        delta_x = random.randint(MIN_HORIZONTAL_DISTANCE, MAX_HORIZONTAL_DISTANCE)
        
        # Calcula la nueva posición x
        x += direction * delta_x

        # Asegurarse de que la plataforma esté dentro de los límites de la ventana
        x = max(0, min(WIDTH - PLATFORM_WIDTH, x))

        platforms.append((x, y))

    return platforms
