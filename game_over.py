import pygame, sys
import random

# Inicializar pygame
pygame.init()

def game_over_menu():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        
        font = pygame.font.SysFont(None, 48)
        text = font.render("Game Over - Press BACK to return to main menu", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        
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
            #elif event.type == pygame.KEYDOWN:
            #    if event.key == pygame.K_BACKSPACE:
                    return  # Retorna al bucle principal del juego

        #screen.fill(BACKGROUND_COLOR)
        #screen.blit(text, text_rect)
        #pygame.display.blit()
        pygame.display.update()
