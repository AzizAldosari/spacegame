import pygame


class Bullet:
    def __init__(self, position, bullet_type, image):
        self.position = pygame.math.Vector2(position)
        self.direction = pygame.math.Vector2(0, -1)  # the bullets move upwards
        self.speed = 7
        self.bullet_type = bullet_type
        self.image = image
        self.rect = self.image.get_rect(center=self.position)

    def update(self):
        self.position += self.direction * self.speed
        # Updates the rect position every time the bullet is updated
        self.rect.center = self.position

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
