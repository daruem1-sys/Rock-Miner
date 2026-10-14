import pygame
import random
from logger import log_event
from circleshape import CircleShape
from ammo import Ammo
from constants import LINE_WIDTH
from constants import ASTEROID_MIN_RADIUS

class Asteroid(CircleShape):

	def __init__(self, x: float, y: float, radius: float) -> None:
		super().__init__(x, y, radius)

	def draw(self, screen):
		pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

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
