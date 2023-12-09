import pygame
import sys
from manual_save import manual_save


def pause_menu(screen, score, kills, level, skills):
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False  # Continue the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Display pause menu options
        screen.fill((0, 0, 0))  # Fill the screen with black to indicate a paused state
        font = pygame.font.Font(None, 74)
        continue_text = font.render('Continue', True, (255, 255, 255))
        save_text = font.render('Save', True, (255, 255, 255))
        exit_text = font.render('Exit', True, (255, 255, 255))

        # Define button rectangles
        continue_button = continue_text.get_rect(center=(400, 200))
        save_button = save_text.get_rect(center=(400, 300))
        exit_button = exit_text.get_rect(center=(400, 400))

        # Draw buttons
        screen.blit(continue_text, continue_button)
        screen.blit(save_text, save_button)
        screen.blit(exit_text, exit_button)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Check for button clicks
        if continue_button.collidepoint(mouse):
            if click[0] == 1:
                pause = False
        elif save_button.collidepoint(mouse):
            if click[0] == 1:
                # Call the manual save function with the current game state
                manual_save(level, score, kills, ','.join(skills))
                print("Game manually saved.")
        elif exit_button.collidepoint(mouse):
            if click[0] == 1:
                pygame.quit()
                sys.exit()

        pygame.display.update()


