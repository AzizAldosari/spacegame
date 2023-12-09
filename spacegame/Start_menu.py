# start_menu.py
import pygame
import pandas as pd
import sys


def draw_controls(screen):
    # Define colors
    WHITE = (255, 255, 255)
    # Set up the fonts for the tutorial
    small_font = pygame.font.Font(None, 36)
    controls_text = [
        "Controls:",
        "Move: Arrow keys",
        "Shoot: Space bar",
        "pause menu: esc",
        "warning:",
        "be careful of the",
        "bosses punches"


    ]

    # Define the top right corner for the tutorial
    top_right_corner = (screen.get_width() - 220, 10)

    # Draw each line of text
    for i, line in enumerate(controls_text):
        text_surface = small_font.render(line, True, WHITE)
        screen.blit(text_surface, (top_right_corner[0], top_right_corner[1] + i * 30))


def show_start_menu(screen):
    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Define font
    font = pygame.font.Font(None, 74)

    # Define text
    title_text = font.render('Space Game', True, WHITE)
    continue_text = font.render('Continue', True, WHITE)
    new_game_text = font.render('New Game', True, WHITE)
    load_game_text = font.render('Load Game', True, WHITE)
    exit_text = font.render('Exit', True, WHITE)

    # Define button rectangles
    continue_button_rect = continue_text.get_rect(center=(400, 200))
    new_game_button_rect = new_game_text.get_rect(center=(400, 300))
    load_game_button_rect = load_game_text.get_rect(center=(400, 400))
    exit_button_rect = exit_text.get_rect(center=(400, 500))

    menu_running = True
    action = None
    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button_rect.collidepoint(event.pos):
                    action = 'continue'
                    menu_running = False
                elif new_game_button_rect.collidepoint(event.pos):
                    action = 'new_game'
                    menu_running = False
                elif load_game_button_rect.collidepoint(event.pos):
                    action = 'load_game'
                    menu_running = False
                elif exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            return action
        screen.fill(BLACK)
        screen.blit(title_text, (400 - title_text.get_width() // 2, 100))
        screen.blit(continue_text, continue_button_rect.topleft)
        screen.blit(new_game_text, new_game_button_rect.topleft)
        screen.blit(load_game_text, load_game_button_rect.topleft)
        screen.blit(exit_text, exit_button_rect.topleft)
        # to draw the controls on screen
        draw_controls(screen)
        pygame.display.flip()
