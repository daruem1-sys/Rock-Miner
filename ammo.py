import pygame
from circleshape import CircleShape

class Ammo(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, 20)  # radius 20 for ammo circle
        self.image = pygame.image.load("assets/ammo.png").convert_alpha()
        self.rect = self.image.get_rect(center=self.position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)  

    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = self.position    