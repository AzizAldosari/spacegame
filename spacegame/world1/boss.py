# due to this game being in real-time and min-max algrithm would not work that would in real time. it is more used
# in turn based games. this boss ai uses utility based system where the boss evalutes the state(speed) and it own health
# then deicde which action to take. the reason speed matters because of the debuff system.
import pygame
from pygame.math import Vector2
import time
from .Laser import Laser
import random




def on_screen(position):
    screen_width, screen_height = pygame.display.get_surface().get_size()
    return 0 <= position.x <= screen_width and 0 <= position.y <= screen_height


class Boss:

    def __init__(self, position, hp, image_path, laser_image_path):
        self.dodge_cooldown = 2 # the shrinking, and streching ablity has a 2 second cooldown, why cause it is cool
        self.last_dodge_time = 0
        self.position = Vector2(position)
        self.hp = hp
        self.original_hp = hp  # Store the original HP for percentage calculations
        self.speed = 2
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=self.position)
        self.laser_cooldown = 0  # Can use laser at 80% HP
        self.last_laser_time = time.time()
        self.laser_fire_rate = 4  # seconds between laser fires
        self.next_laser_time = time.time() + self.laser_fire_rate
        self.laser_image_path = laser_image_path
        self.lasers = []  # Store lasers fired by the boss
        pygame.time.set_timer(pygame.USEREVENT + 3, 2000)  # Set up laser fire event to occur every 2 seconds
        self.rect = self.image.get_rect(center=self.position)
        self.self_healing_rate = 20  # Amount of HP regained
        self.heal_cooldown = 10  # Cooldown in seconds for self-healing
        self.last_heal_time = time.time()
        self.original_image = self.image.copy()  # Store the original image
        self.original_rect_size = self.rect.size  # Store the original rect size

    # to prevent the boss from running away and not giving an ending
    def check_bounds(self):
        screen_width, screen_height = pygame.display.get_surface().get_size()

        # Check and adjust left and right bounds
        if self.rect.left < 0:
            self.rect.left = 0
            self.speed = -self.speed  # Change direction if hitting the left boundary
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
            self.speed = -self.speed  # Change direction if hitting the right boundary

        # Check and adjust top and bottom bounds
        if self.rect.top < 0:
            self.rect.top = 0
            self.speed = -self.speed  # Change direction if hitting the top boundary
        elif self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.speed = -self.speed  # Change direction if hitting the bottom boundary

        # Update the position attribute based on the adjusted rect
        self.position = Vector2(self.rect.center)

    def check_near_border(self):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        if self.rect.left < 100 or self.rect.right > screen_width - 100 or \
                self.rect.top < 100 or self.rect.bottom > screen_height - 100:
            self.speed = -self.speed

    def decide_action(self, player, player_bullets):
        current_time = time.time()
        self.decide_movement(player)

        # Check for nearby player bullets and dodge
        if self.is_bullet_nearby(player_bullets):
            self.dodge()

        # Laser action
        if self.hp <= self.original_hp * 0.8 and current_time - self.last_laser_time > self.laser_cooldown:
            self.fire_laser(player.position)
            self.last_laser_time = current_time

        # Self-healing action
        self.self_heal()

    def fire_laser(self, player_position):
        current_time = time.time()
        if current_time >= self.next_laser_time:
            direction = player_position - self.position
            direction = direction.normalize()  # Normalize the direction vector
            new_laser = Laser(self.position, direction, self.laser_image_path)
            self.lasers.append(new_laser)
            self.next_laser_time = current_time + self.laser_fire_rate

    def draw_health_bar(self, screen):
        # Health bar position and size
        bar_x = self.rect.x
        bar_y = self.rect.y - 20
        bar_width = self.rect.width
        bar_height = 10

        # Background of the health bar
        background_bar = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(screen, (128, 128, 128), background_bar)  # Gray color for background

        # Health portion of the health bar
        health_ratio = self.hp / self.original_hp
        health_bar_width = bar_width * health_ratio  # Calculate width based on health ratio
        health_bar = pygame.Rect(bar_x, bar_y, health_bar_width, bar_height)

        # Change color depending on health ratio (Green to Red)
        if health_ratio > 0.5:
            color = (0, 255, 0)  # Green
        elif health_ratio > 0.25:
            color = (255, 255, 0)  # Yellow
        else:
            color = (255, 0, 0)  # Red

        pygame.draw.rect(screen, color, health_bar)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        self.draw_health_bar(screen)  # Draw the health bar

    def update(self, player, screen, player_bullets):
        current_time = time.time()
        self.decide_action(player, player_bullets)
        self.check_bounds()

        if current_time - self.last_laser_time > 2:  # the boss fires every 2 seconds
            self.fire_laser(player.position)
            self.last_laser_time = current_time

        # Update all lasers
        for laser in self.lasers:
            laser.update()
            laser.draw(screen)

        # Remove lasers that have gone off screen
        self.lasers = [laser for laser in self.lasers if on_screen(laser.position)]

        # Draw lasers
        for laser in self.lasers:
            laser.draw(screen)

    def is_bullet_nearby(self, player_bullets):
        # Define a safety zone around the boss for bullet detection
        safety_margin = 100
        danger_zone = self.rect.inflate(safety_margin, safety_margin)

        # Check if any player bullet is within the danger zone
        for bullet in player_bullets:
            if danger_zone.colliderect(bullet.rect):
                return True
        return False

    def decide_movement(self, player):

        #  Move towards player if boss HP is low, else move away
        if self.hp < self.original_hp * 0.1:
            # Move towards player
            self.move_towards(player.position)
        else:
            # Move away from player
            self.move_away(player.position)

    def move_towards(self, target_position):
        # Move towards a target position
        direction = target_position - self.position
        if direction.length() > 0:
            direction = direction.normalize()

        self.position += direction * self.speed
        self.update_rect()

    def move_away(self, target_position):
        # Move away from a target position
        direction = self.position - target_position
        if direction.length() > 0:
            direction = direction.normalize()

        self.position += direction * self.speed
        self.update_rect()

    def dodge(self):
        current_time = time.time()
        if current_time - self.last_dodge_time > self.dodge_cooldown:
            dodge_horizontal = random.choice([True, False])
            new_size = (self.rect.width - 20, self.rect.height + 20) if dodge_horizontal else (
                self.rect.width + 20, self.rect.height - 20)
            # Ensure new size is never negative, so it wouldn't crash
            new_size = (max(10, new_size[0]), max(10, new_size[1]))
            self.rect.size = new_size
            self.image = pygame.transform.scale(self.original_image, new_size)
            self.last_dodge_time = current_time
            pygame.time.set_timer(pygame.USEREVENT + 2, 2000)  # Reset shape timer

    def reset_shape(self):
        self.rect.size = self.original_rect_size
        self.image = self.original_image.copy()

    def self_heal(self):
        # Heal the boss if HP is below a certain hp and cooldown has passed
        current_time = time.time()
        if self.hp < self.original_hp * 0.4 and current_time - self.last_heal_time > self.heal_cooldown:
            self.hp += self.self_healing_rate
            self.hp = min(self.hp, self.original_hp)  # Ensure HP does not exceed original HP
            self.last_heal_time = current_time

    def update_rect(self):
        screen_width, _ = pygame.display.get_surface().get_size()
        self.position.x = max(0, min(screen_width - self.rect.width, self.position.x))
        self.rect.center = self.position
