from constants import PLAYER_RADIUS
from constants import LINE_WIDTH
from constants import PLAYER_TURN_SPEED
from circleshape import CircleShape
from constants import ACCELERATION
from constants import BREAKING
from constants import SCREEN_WIDTH
from constants import SCREEN_HEIGHT
from shot import Shot
from constants import SHOT_RADIUS
from constants import PLAYER_SHOOT_SPEED
from constants import PLAYER_SHOOT_COOLDOWN_TIMER
import pygame # type: ignore import of the game modual

class Player(CircleShape):
	def __init__(self, x, y):
		super().__init__(x, y, PLAYER_RADIUS)
		pygame.font.init()
		self.rotation = 0
		self.idle_frames = [
			pygame.image.load("assets/ship_idle.png").convert_alpha()
		]
		self.thrust_frames = [
			pygame.image.load("assets/ship_thurst1.png").convert_alpha(),
			pygame.image.load("assets/ship_thrust2.png").convert_alpha(),
			pygame.image.load("assets/ship_thrust3.png").convert_alpha()
		]
		self.current_frames = self.idle_frames
		self.frame_index = 0
		self.animation_speed = 8
		self.image = self.current_frames[0]
		self.new_frames = self.idle_frames
		self.rect = self.image.get_rect(center=(x, y))
		self.velocity = pygame.Vector2(0, 0)
		self.gun_ammo = 100
		self.missle_ammo = 0
		self.shot_cooldown = 0
		self.font = pygame.font.Font(None, 36)

	#def triangle(self) -> list[pygame.Vector2]:
		#forward = pygame.Vector2(0, 1).rotate(self.rotation)
		#right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
		#a = self.position + forward * self.radius
		#b = self.position - forward * self.radius - right
		#c = self.position - forward * self.radius + right
		#return [a, b, c]

	def draw(self, screen):
		# pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
		rotated_sprite = pygame.transform.rotate(self.image, -self.rotation)
		rect = rotated_sprite.get_rect(center=self.position)
		screen.blit(rotated_sprite, rect)
		#Text below this line
		text_surface = self.font.render(f"Gun Ammunition: {self.gun_ammo} Missle Ammunition {self.missle_ammo}", False, "white")
		screen.blit(text_surface, (10, 10))

	def rotate(self, dt):
		self.rotation += PLAYER_TURN_SPEED * dt

	def update(self, dt: float) -> None:
		keys = pygame.key.get_pressed()

		if keys[pygame.K_a]:
			self.rotate(-dt)
		if keys[pygame.K_d]:
			self.rotate(dt)
		if keys[pygame.K_w]:
			self.move(dt)
			self.new_frames = self.thrust_frames
		else:
			self.new_frames = self.idle_frames
		if keys[pygame.K_s]:
			self.reverse(dt)
		if keys[pygame.K_x]:
			self.stop(dt)
		if keys[pygame.K_SPACE]:
			if self.shot_cooldown < 0:
				if self.gun_ammo > 0:
					self.shoot()
					self.shot_cooldown += PLAYER_SHOOT_COOLDOWN_TIMER
					self.gun_ammo -= 1
			else:
				self.shot_cooldown -= dt

		self.position.y %= SCREEN_HEIGHT
		self.position.x %= SCREEN_WIDTH
		self.position += self.velocity * dt
		if self.new_frames != self.current_frames:
			self.current_frames = self.new_frames
		self.frame_index += self.animation_speed * dt
		if self.frame_index >= len(self.current_frames):
			self.frame_index = 0
		
		self.image = self.current_frames[int(self.frame_index)]

	def move(self, dt):
		unit_vector = -pygame.Vector2(0, 1)
		rotated_vector = unit_vector.rotate(self.rotation)
		self.velocity += rotated_vector * ACCELERATION * dt

	def reverse(self, dt):
		backwards = pygame.Vector2(0, 1).rotate(self.rotation)
		self.velocity += backwards * (ACCELERATION / 2) * dt

	def stop(self, dt):
		speed = self.velocity.length()
		unit_vector = pygame.Vector2(0, 1)
		rotated_vector = unit_vector.rotate(self.rotation)
		if speed > 0:
			new_speed = max(0, speed - BREAKING * dt)
			self.velocity.scale_to_length(new_speed)

	def shoot(self):	
		shot = Shot(self.position.x, self.position.y)
		shot_vector = pygame.Vector2(0, -1)
		rotated_vector = shot_vector.rotate(self.rotation)
		shot.velocity = rotated_vector * PLAYER_SHOOT_SPEED
		shot_sound = pygame.mixer.Sound("assets/shot.wav")
		shot_sound.set_volume(0.5)
		shot_sound.play()


