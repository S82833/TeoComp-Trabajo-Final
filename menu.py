import pygame, sys
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Menu")

BG = pygame.image.load("square/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    #Estilo de letra 
    return pygame.font.Font("square/font.ttf", size)

def play():
    while True:
        PLAY_BALL = Button(game_loop())
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        #PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        #PLAY_RECT = PLAY_BALL.get_rect(center=(200, 400))
        SCREEN.blit(PLAY_BALL)

        #Button BACK
        PLAY_BACK = Button(image=None, pos=(800, 800), 
                            text_input="BACK", font=get_font(20), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        OPTIONS_TEXT = get_font(30).render("*El juego consistira en la constante persecusion hacia el jugador", True, "white")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(400, 250))
        OPTIONS_TEXT1 = get_font(30).render("*El jugador podra acabar con su enemigo consumiendo la pastilla amarilla", True, "white")
        OPTIONS_RECT1 = OPTIONS_TEXT1.get_rect(center=(400, 210))
        OPTIONS_TEXT2 = get_font(30).render("*Se podra pasar de nivel en la ultima plataforma", True, "white")
        OPTIONS_RECT2 = OPTIONS_TEXT2.get_rect(center=(400, 290))
        OPTIONS_TEXT3 = get_font(30).render("*Tendras que presionar la tecla E del teclado", True, "white")
        OPTIONS_RECT3= OPTIONS_TEXT2.get_rect(center=(400, 330))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        SCREEN.blit(OPTIONS_TEXT1, OPTIONS_RECT1)
        SCREEN.blit(OPTIONS_TEXT2, OPTIONS_RECT2)
        SCREEN.blit(OPTIONS_TEXT3, OPTIONS_RECT3)

        OPTIONS_BACK = Button(image=None, pos=(400, 650), 
                            text_input="BACK", font=get_font(50), base_color="White", hovering_color="Blue")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0)) 

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(170).render("HOP SQUARE", True, "#000000")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("square/Play Rect.png"), pos=(400, 250), 
                             text_input="Play", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("square/Options Rect.png"), pos=(400, 400), 
                            text_input="RulesS", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("square/Quit Rect.png"), pos=(400, 550), 
                            text_input="QUIT", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.update()
