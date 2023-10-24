import pygame
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
BACKGROUND_COLOR = (50, 50, 50)
PLAYER_COLOR = (0, 255, 0)
ENEMY_COLOR = (255, 0, 0)
PLATFORM_COLOR = (100, 100, 100)
LAST_PLATFORM_COLOR = (0, 0, 255)  # Color para la última plataforma
ENEMY_VISION_RANGE = 100
ENEMY_INCREMENT_SPEED = 0.1
SAFE_ZONE = 150  # Distancia segura alrededor del jugador donde los enemigos no pueden aparecer al inicio
VISION_RANGE = 150  # Rango de visión del enemigo
POWERUP_SIZE = 30
POWERUP_COLOR = (255, 255, 0)  # Amarillo, como en Pac-Man
POWERUP_DURATION = 2000  # Duración del power-up en milisegundos
CURRENT_LEVEL = 1
# Configurar la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Automaton Runner')

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


FONT = pygame.font.SysFont(None, 36)  # Inicializa la fuente.
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
                        # Reiniciar el juego
                        CURRENT_LEVEL = 1
                        game_loop()
                    
        # Dibujar todo
        screen.fill(BACKGROUND_COLOR)
        if powerup:
            powerup.draw(screen)
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for i, platform in enumerate(platforms):
            if i == len(platforms) - 1:  # Si es la última plataforma
                color = LAST_PLATFORM_COLOR
            else:
                color = PLATFORM_COLOR
            pygame.draw.rect(screen, color, (platform[0], platform[1], PLATFORM_WIDTH, PLATFORM_HEIGHT))

        # Dibuja el nivel actual en la pantalla
        font = pygame.font.SysFont(None, 36)
        level_text = font.render(f'Level: {CURRENT_LEVEL}', True, (255, 255, 255))
        screen.blit(level_text, (10, 10))
        
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

# Llamar a la función principal del juego
game_loop()