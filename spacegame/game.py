import pygame
from Start_menu import show_start_menu
import new_game
import continue_game
import Load_game
from world1.world1 import run_world1
import win_screen
import gameover_screen


# from world2.world2 import run_world2 # no world2 due to time but future thing to do

# def run_world2(screen):
#   pass


def main():
    #  global world2
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Space Game')

    current_state = 'start_menu'
    player_score = 0
    player_level = 1
    player_world = 1
    player_kills = 0

    while True:
        if current_state == 'start_menu':
            choice = show_start_menu(screen)
            if choice == 'new_game':
                current_state = 'world1'
                new_game.run(screen)
            elif choice == 'continue':
                current_state = 'world1'
                continue_game.run(screen)
            elif choice == 'load_game':
                current_state = 'world1'
                Load_game.run(screen)
            elif choice == 'exit':
                running = False  # Exit the game loop

        elif current_state == 'world1':
            boss_defeated, player_score, player_level, player_kills = run_world1(screen)
            if boss_defeated:
                try:
                    current_state = 'winning'
                except ImportError:
                    current_state = 'winning'
            else:
                current_state = 'game_over'

        # elif current_state == 'world2':
        # game_completed, player_dead = run_world2(screen)
        #  if game_completed:
        #     current_state = 'winning'
        # elif player_dead:
        #   current_state = 'game_over'

        elif current_state == 'winning':
            win_screen.win_screen(screen, player_score, player_level, 1, player_kills)
            current_state = 'start_menu'

        elif current_state == 'game_over':
            gameover_screen.game_over_screen(screen, player_score, player_level, 1, player_kills)
            current_state = 'start_menu'

            pygame.display.flip()
            pygame.time.Clock().tick(60)


if __name__ == '__main__':  # Quit pygame after exiting the loop
    main()
