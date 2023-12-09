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
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check if the mouse is clicked on the save button
                if save_button.collidepoint(mouse_pos):
                    # Call the manual save function with the current game state
                    manual_save(level, score, kills, ','.join(skills))
                    print("Game manually saved.")
                elif continue_button.collidepoint(mouse_pos):
                    pause = False
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        # Display pause menu options
        screen.fill((0, 0, 0))  # Fill the screen with black to show that the user is in the pause screen
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

        pygame.display.update()
