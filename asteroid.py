import pygame # type: ignore import of the game modual
import random
from logger import log_event
from circleshape import CircleShape
from ammo import Ammo
from constants import LINE_WIDTH
from constants import ASTEROID_MIN_RADIUS

class Asteroid(CircleShape):

	def __init__(self, x: float, y: float, radius: float) -> None:
		super().__init__(x, y, radius)
		ASTEROID_IMAGE_SMALL = pygame.image.load("assets/asteroid_small.png").convert_alpha()
		ASTEROID_IMAGE_MEDIUM = pygame.image.load("assets/asteroid_medium.png").convert_alpha()
		ASTEROID_IMAGE_LARGE = pygame.image.load("assets/asteroid_large.png").convert_alpha()
		if radius <= ASTEROID_MIN_RADIUS:
			self.image = ASTEROID_IMAGE_SMALL
		elif radius <= ASTEROID_MIN_RADIUS * 2:
			self.image = ASTEROID_IMAGE_MEDIUM
		else:
			self.image = ASTEROID_IMAGE_LARGE
	def draw(self, screen):
		pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)
		rect = self.image.get_rect(center=(self.position.x, self.position.y))
		screen.blit(self.image, rect)

	def update(self, dt):
		self.position += self.velocity * dt

	def split(self):
		self.kill()
		if self.radius <= ASTEROID_MIN_RADIUS:
			random_ammo = random.randint(1, 10)
			if random_ammo == 1:  # 10% chance to drop ammo
				log_event("ammo_drop")
				new_ammo = Ammo(self.position.x, self.position.y)
				new_ammo.velocity = self.velocity.rotate(random.uniform(20, 50)) * 0.75
				return
		if self.radius > ASTEROID_MIN_RADIUS:
			angle = random.uniform(20, 50)
			new_radius = self.radius - ASTEROID_MIN_RADIUS
			log_event("asteroid_split")
			new_asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
			new_asteroid1.velocity = self.velocity.rotate(angle) * 1.2
			new_asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
			new_asteroid2.velocity = self.velocity.rotate(-angle) * 1.2
