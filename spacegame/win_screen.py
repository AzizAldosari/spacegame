import pygame
import sys


def win_screen(screen, player_score, player_level, player_world, player_kills):
    pygame.font.init()
    font = pygame.font.SysFont(None, 74)
    small_font = pygame.font.SysFont(None, 50)

    # Texts
    game_over_text = font.render('winning', True, (255, 0, 0))
    score_text = small_font.render(f'Score: {player_score}', True, (255, 255, 255))
    level_text = small_font.render(f'Level: {player_level}', True, (255, 255, 255))
    world_text = small_font.render(f'World: {player_world}', True, (255, 255, 255))
    kills_text = small_font.render(f'Kills: {player_kills}', True, (255, 255, 255))
    main_menu_text = small_font.render('Main Menu', True, (255, 255, 255))
    exit_text = small_font.render('Exit', True, (255, 255, 255))

    # Main loop for the game over screen
    running = True
    while running:
        screen.fill((0, 0, 0))  # Fill the screen with black

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if main_menu_button.collidepoint(mouse_pos):
                    return 'main_menu'
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        # Positioning the text
        screen.blit(game_over_text, (200, 50))
        screen.blit(score_text, (250, 150))
        screen.blit(level_text, (250, 200))
        screen.blit(world_text, (250, 250))
        screen.blit(kills_text, (250, 300))

        # Buttons
        main_menu_button = screen.blit(main_menu_text, (250, 400))
        exit_button = screen.blit(exit_text, (450, 400))

        pygame.display.flip()