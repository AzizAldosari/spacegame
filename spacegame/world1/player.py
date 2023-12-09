import pygame
import random
from .Bullet import Bullet


class Player:
    def __init__(self, images, bullet_images, start_speed, skill_image):
        self.position = pygame.math.Vector2(100, 100)
        self.speed = 5
        self.hp = 100
        self.level = 1
        self.experience = 0
        self.skills = {
            'speed_boost': False,
            'power_shot': False,
            'extra_hp': False,
            'elemental_power': False,
        }
        self.images = images
        self.bullet_images = bullet_images
        self.bullet_type = 'normal'
        self.bullets = []
        self.speed = start_speed
        self.original_speed = start_speed  # Store the original speed for resetting after debuffs
        self.image = self.images['normal']
        self.rect = self.image.get_rect(topleft=self.position)
        self.skill_images = {}
        for skill, path in skill_image.items():
            self.skill_images[skill] = pygame.image.load(path)

    def reset_speed(self):
        self.speed = self.original_speed

    # Movement methods
    def move_left(self):
        self.position.x -= self.speed

    def move_right(self):
        self.position.x += self.speed

    def move_up(self):
        self.position.y -= self.speed

    def move_down(self):
        self.position.y += self.speed

    # Shooting method
    def shoot(self):
        # Allow shooting only if there are no bullets on screen
        if not self.bullets:
            bullet_type = self.bullet_type if self.bullet_type in self.bullet_images else 'normal'
            bullet = Bullet(self.position, bullet_type, self.bullet_images[bullet_type])
            self.bullets.append(bullet)

    # Level up and skill selection
    def level_up(self):
        self.level += 1
        self.experience = 0
        self.present_skill_options()

    def present_skill_options(self):
        normal_skills = ['speed_boost', 'power_shot', 'extra_hp']
        special_skills = ['elemental_power']
        weighted_skills = normal_skills * 99 + special_skills * 1
        self.skill_choices = random.sample(weighted_skills, 3)
        self.select_skill()

    def select_skill(self):
        # This method will displays a simple GUI where the player can select a skill
        screen = pygame.display.get_surface()  # Get the current display surface
        skill_surfaces = [self.skill_images[skill] for skill in self.skill_choices]

        # Create rectangles for skill images for click detection
        skill_rects = []
        for i, skill in enumerate(skill_surfaces):
            rect = skill.get_rect(topleft=(50 + i * 100, 100))
            skill_rects.append(rect)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(skill_rects):
                        if rect.collidepoint(mouse_pos):
                            self.apply_skill(self.skill_choices[i])
                            running = False
                elif event.type is pygame.QUIT:
                    pygame.quit()
                    exit()

            screen.fill((0, 0, 0))  # Clear screen
            for i, skill_surface in enumerate(skill_surfaces):
                # Draw skill images at certain positions
                screen.blit(skill_surface, (50 + i * 100, 100))

            pygame.display.flip()  # Update the display

    def apply_skill(self, chosen_skill):
        if chosen_skill in self.skills and not self.skills[chosen_skill]:
            self.skills[chosen_skill] = True
            if chosen_skill == 'speed_boost':
                self.speed += 2
            elif chosen_skill == 'power_shot':
                self.bullet_type = 'power'
            elif chosen_skill == 'extra_hp':
                self.hp += 50
            elif chosen_skill == 'elemental_power':
                self.bullet_type = 'elemental'

    def draw_hp_bar(self, screen, position, size):
        # Draw a background for the HP bar
        bg_rect = pygame.Rect(position, size)
        pygame.draw.rect(screen, (255, 0, 0), bg_rect)  # Red background for HP

        # Draw the foreground for the HP bar
        hp_width = (self.hp / 100) * size[0]
        hp_rect = pygame.Rect(position, (hp_width, size[1]))
        pygame.draw.rect(screen, (0, 255, 0), hp_rect)  # Green foreground for HP

    def draw_exp_bar(self, screen, position, size, exp_to_next_level):
        # Draw a background for the EXP bar
        bg_rect = pygame.Rect(position, size)
        pygame.draw.rect(screen, (128, 128, 128), bg_rect)  # Grey background for EXP

        # Draw the foreground for the EXP bar
        exp_width = (self.experience / exp_to_next_level) * size[0]
        exp_rect = pygame.Rect(position, (exp_width, size[1]))
        pygame.draw.rect(screen, (255, 255, 0), exp_rect)  # Yellow foreground for EXP

    # Drawing method
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        # Update the rect position every time the player is drawn
        self.rect.topleft = self.position

        # Draw the HP and EXP bars
        self.draw_hp_bar(screen, (20, 20), (200, 20))  # Position and size of HP bar
        self.draw_exp_bar(screen, (20, 50), (200, 20),
                          100)  # Position and size of EXP bar
