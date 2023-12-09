# due to this game being in real-time and min-max algrithm would not work that would in real time. it is more used
# in turn based games. this boss ai uses utility based system where the boss evalutes the state(speed) and it own health
# then deicde which action to take. the reason speed matters because of the debuff system.
import pygame
from pygame.math import Vector2
import time
from .Laser import Laser


# import world1


def on_screen(position):
    screen_width, screen_height = pygame.display.get_surface().get_size()
    return 0 <= position.x <= screen_width and 0 <= position.y <= screen_height


class Boss:
    def __init__(self, position, hp, image_path, laser_image_path):
        self.dodge_cooldown = 4
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
        self.self_healing_rate = 10  # Amount of HP regained
        self.heal_cooldown = 10  # Cooldown in seconds for self-healing
        self.last_heal_time = time.time()

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

    def decide_action(self, player):
        current_time = time.time()
        self.decide_movement(player)

        # Laser action
        if self.hp <= self.original_hp * 0.8 and current_time - self.last_laser_time > self.laser_cooldown:
            self.fire_laser(player.position)  # Pass player's position
            self.last_laser_time = current_time

    def fire_laser(self, player_position):
        current_time = time.time()
        if current_time >= self.next_laser_time:
            direction = player_position - self.position
            direction = direction.normalize()  # Normalize the direction vector
            new_laser = Laser(self.position, direction, self.laser_image_path)
            self.lasers.append(new_laser)
            self.next_laser_time = current_time + self.laser_fire_rate

    def dodge(self, player):
        # Dodge by changing shape (adjusting the rect size)
        if self.rect.height > self.rect.width:
            self.rect.inflate_ip(-20, 20)  # Become wider and shorter
        else:
            self.rect.inflate_ip(20, -20)  # Become taller and narrower
        # Set up a timer event to reset shape after 2 seconds
        pygame.time.set_timer(Boss.dodge_reset, 2000)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def update(self, player, screen):
        current_time = time.time()
        self.decide_action(player)
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
        # Dodge by changing shape (adjusting the rect size) with a cooldown
        current_time = time.time()
        if current_time - self.last_dodge_time > self.dodge_cooldown:
            if self.rect.height > self.rect.width:
                self.rect.inflate_ip(-20, 20)  # Become wider and shorter
            else:
                self.rect.inflate_ip(20, -20)  # Become taller and narrower
            self.last_dodge_time = current_time
            # Set up a timer event to reset shape after 2 seconds
            pygame.time.set_timer(pygame.USEREVENT + 2, 2000)

    def update_rect(self):
        screen_width, _ = pygame.display.get_surface().get_size()
        self.position.x = max(0, min(screen_width - self.rect.width, self.position.x))
        self.rect.center = self.position
