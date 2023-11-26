import pygame, sys
import random

# Inicializar pygame
pygame.init()

# Constantes
WIDTH = 800
HEIGHT = 800
PLAYER_SIZE = 50
ENEMY_SIZE = 40
ENEMY_SPEED = 2
PLATFORM_HEIGHT = 20
PLATFORM_WIDTH = 150
SAFE_ZONE = 150  # Distancia segura alrededor del jugador donde los enemigos no pueden aparecer al inicio
CURRENT_LEVEL = 1

# Configurar la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Automaton Runner')

background_image = pygame.image.load("square/fondo_b.png")

# Clases del juego
# Clase para el jugador
# Clase para el enemigo con autómata finito
# Función para generar plataformas sin superposición vertical y con espacios saltables
# Inicializa la fuente.
# Función principal del juego

def game_loop():
    
    global CURRENT_LEVEL
    clock = pygame.time.Clock()
    # Generar enemigos según el nivel
    enemies = []
    
    while len(enemies) < 1 + CURRENT_LEVEL // 5:
        enemy_x = random.randint(0, WIDTH - ENEMY_SIZE)
        enemy_y = random.randint(0, HEIGHT - ENEMY_SIZE)
        
        # Asegurarte de que el enemigo no esté cerca del jugador al inicio
        while abs(enemy_x - WIDTH // 2) < SAFE_ZONE and abs(enemy_y - HEIGHT + PLAYER_SIZE + 10) < SAFE_ZONE:
            enemy_x = random.randint(0, WIDTH - ENEMY_SIZE)
            enemy_y = random.randint(0, HEIGHT - ENEMY_SIZE)

        enemy = Enemy(enemy_x, enemy_y, ENEMY_SPEED)
        enemy.dx += ENEMY_INCREMENT_SPEED * CURRENT_LEVEL
        enemy.dy += ENEMY_INCREMENT_SPEED * CURRENT_LEVEL
        enemies.append(enemy)

    player = Player()
    platforms = generate_platforms()
    powerup = place_powerup_on_platform(platforms)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    last_platform = pygame.Rect(platforms[-1][0], platforms[-1][1], PLATFORM_WIDTH, PLATFORM_HEIGHT)
                    
                    # Ajustar el rectángulo del jugador para dar un margen de error
                    player_rect = pygame.Rect(player.x - 5, player.y - 5, PLAYER_SIZE + 10, PLAYER_SIZE + 10)
                    
                    if player_rect.colliderect(last_platform):
                        CURRENT_LEVEL += 1
                        game_loop()  # Reinicia el juego para el siguiente nivel

        # Mover al jugador y a los enemigos
        player.move(platforms)
        player.check_powerup_duration()  # Verificar la duración del power-up
        if powerup:
            powerup_rect = pygame.Rect(powerup.x, powerup.y, POWERUP_SIZE, POWERUP_SIZE)
        player_rect = pygame.Rect(player.x, player.y, PLAYER_SIZE, PLAYER_SIZE)

        if powerup:  # Asegurarse de que la pastilla existe antes de verificar la colisión
            powerup_rect = pygame.Rect(powerup.x, powerup.y, POWERUP_SIZE, POWERUP_SIZE)
            if player_rect.colliderect(powerup_rect) and not player.powered_up:
                player.activate_powerup()
                powerup = None  # Elimina la pastilla del juego

        for enemy in enemies:
            enemy.move(player)
            
            # Verificar colisión entre enemigo y jugador
            enemy_rect = pygame.Rect(enemy.x, enemy.y, ENEMY_SIZE, ENEMY_SIZE)
            player_rect = pygame.Rect(player.x, player.y, PLAYER_SIZE, PLAYER_SIZE)
            if player_rect.colliderect(enemy_rect):
                if player.powered_up:
                    enemies.remove(enemy)  # Eliminar al enemigo si el jugador tiene el power-up
                else:
                    player.times_hit += 1
                    if player.times_hit == 3: 
                        # Muestra el menú de Game Over
                        game_over_menu()
                    
        # Dibujar todo
        screen.blit(background_image, (0, 0))

        if powerup:
            powerup.draw(screen)
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        LAST_PLATFORM_IMAGE = pygame.image.load("square/imagen_last_platform.png")
        PLATFORM_IMAGE = pygame.image.load("square/imagen_platform.png")  


        for i, platform in enumerate(platforms):
            if i == len(platforms) - 1:  # Si es la última plataforma
                image = LAST_PLATFORM_IMAGE
            else:
                image = PLATFORM_IMAGE
                
            # Dibuja la imagen en lugar del rectángulo de color
            screen.blit(image, (platform[0], platform[1]))

        # Dibuja el nivel actual en la pantalla
        font = pygame.font.SysFont(None, 36)
        level_text = font.render(f'Level: {CURRENT_LEVEL}', True, (255, 255, 255))
        screen.blit(level_text, (10, 10))
        
        pygame.display.flip()

        clock.tick(60)
