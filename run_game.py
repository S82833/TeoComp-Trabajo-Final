def run_game():
    while True:
        choice = main_menu()

        if choice == "PLAY":
            # Llamar a la función principal del juego
            game_loop()
        elif choice == "RULES":
            options()
        elif choice == "QUIT":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    #pygame.init()
    run_game()
