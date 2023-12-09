import pygame
from pygame.math import Vector2


class Enemy1:
    def __init__(self, position, speed, image_path):
        self.position = Vector2(position)
        self.speed = speed
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=self.position)

    def update(self, player_position, bullets):
        # A simple AI that moves towards the player's current position
        direction = Vector2(player_position) - self.position
        if direction.length() > 0:  # Avoid division by zero
            direction = direction.normalize()

        # Basic decision-making tree
        move_direction = self.decide_movement(direction, bullets)

        # Move the enemy
        self.position += move_direction * self.speed
        self.rect.center = self.position

    def decide_movement(self, player_direction, bullets):
        # Start with moving towards the player
        move_direction = player_direction

        # Check for nearby bullets and adjust move direction to dodge
        for bullet in bullets:
            if self.is_bullet_close(bullet):
                # Calculate a dodge direction
                dodge_direction = self.calculate_dodge_direction(bullet)
                move_direction += dodge_direction
                # Ensure the enemy does not move too fast after combining directions
        if move_direction.length() > 0:
            move_direction = move_direction.normalize()

        return move_direction

    def is_bullet_close(self, bullet):
        # Define a "danger zone" distance
        danger_zone = 200
        return self.position.distance_to(bullet.position) < danger_zone

    def calculate_dodge_direction(self, bullet):
        # Calculate direction vector from bullet to enemy
        direction_from_bullet = self.position - bullet.position

        # Check if the bullet is to the left or right and above or below the enemy
        if direction_from_bullet.x > 0:
            dodge_x = 1  # Dodge right if bullet is to the left
        else:
            dodge_x = -1  # Dodge left if bullet is to the right

        if direction_from_bullet.y > 0:
            dodge_y = 1  # Dodge down if bullet is above
        else:
            dodge_y = -1  # Dodge up if bullet is below

        dodge_direction = Vector2(dodge_x, dodge_y)
        return dodge_direction.normalize()

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


