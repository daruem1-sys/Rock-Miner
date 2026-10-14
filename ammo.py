import pygame # type: ignore import of the game modual
from circleshape import CircleShape
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Ammo(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, 20)  # radius 20 for ammo circle
        self.image = pygame.image.load("assets/ammo.png").convert_alpha()
        self.rect = self.image.get_rect(center=self.position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)  

    def update(self, dt):
        self.position.y %= SCREEN_HEIGHT
        self.position.x %= SCREEN_WIDTH
        self.position += self.velocity * dt
        self.rect.center = self.position    