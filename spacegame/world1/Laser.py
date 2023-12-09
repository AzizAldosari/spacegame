import pygame
from pygame.math import Vector2


class Laser:
    def __init__(self, position, direction, image_path, speed=20):
        self.position = Vector2(position)
        self.direction = Vector2(direction).normalize()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=self.position)
        self.speed = speed

    def update(self):
        self.position += self.direction * self.speed
        self.rect.center = self.position

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
