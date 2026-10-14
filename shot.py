import pygame
from constants import SHOT_RADIUS
from circleshape import CircleShape
from constants import LINE_WIDTH

class Shot(CircleShape):

	def __init__(self, x: float, y: float):
		super().__init__(x, y, SHOT_RADIUS)
		self.sprite = pygame.image.load("assets/shot.png").convert_alpha()
		
	def draw(self, screen) -> None:
		angle = pygame.Vector2(0, -1).angle_to(self.velocity)
		rotated_sprite = pygame.transform.rotate(self.sprite, -angle)
		rect = rotated_sprite.get_rect(center=self.position)
		screen.blit(rotated_sprite, rect)

	def update(self, dt) -> None:
		self.position += self.velocity * dt
		