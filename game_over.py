import pygame, sys
import random

# Inicializar pygame
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Automaton Runner')

background_image = pygame.image.load("square/fondo_b.png")


FONT = pygame.font.SysFont(None, 36)  # Inicializa la fuente.
# Función principal del juego

def game_over_menu():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        
        BACK_BUTTON = Button(image=None, pos=(400, 300), 
                              text_input="RETURN", font=get_font(50), base_color="White", hovering_color="Blue")

        BACK_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        BACK_BUTTON.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

                    return  # Retorna al bucle principal del juego

        pygame.display.update()

