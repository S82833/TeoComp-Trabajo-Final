import pygame, sys
import random

# Inicializar pygame
pygame.init()

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
# Función de game_loop()
def run_game():
    while True:
        choice = main_menu()

        if choice == "PLAY":
            # Llamar a la función principal del juego
            game_loop()
        elif choice == "RULES":
            #Llamar a la funcion de lectura a reglas
            options()
        elif choice == "QUIT":
            #Salir del juego
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    #pygame.init()
    run_game()
