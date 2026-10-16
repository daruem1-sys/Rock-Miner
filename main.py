import pygame
import sys
from constants import SCREEN_WIDTH
from constants import SCREEN_HEIGHT
from logger import log_state
from logger import log_event
from player import Player
from asteroid import Asteroid
from ammo import Ammo
from asteroidfield import AsteroidField
from shot import Shot

def main():
	print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
	print(f"Screen width: {SCREEN_WIDTH}")
	print(f"Screen height: {SCREEN_HEIGHT}")
	pygame.init()
	pygame.mixer.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	clock = pygame.time.Clock()
	dt = 0.0
	updatable = pygame.sprite.Group()
	drawable = pygame.sprite.Group()
	asteroids = pygame.sprite.Group()
	ammo = pygame.sprite.Group()
	shots = pygame.sprite.Group()
	AsteroidField.containers = (updatable)
	Player.containers = (updatable, drawable)
	Asteroid.containers = (asteroids, updatable, drawable)
	Ammo.containers = (ammo, updatable, drawable)
	Shot.containers = (shots, updatable, drawable)
	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
	asteroidfield = AsteroidField()
	while True:
		log_state()
		updatable.update(dt)
		for asteroid in asteroids:
			if asteroid.collides_with(player):
				log_event("player_hit")
				print("Game over!")
				sys.exit()
			for shot in shots:
				if shot.collides_with(asteroid):
					log_event("asteroid_shot")
					asteroid.split()
					shot.kill()
		for ammoo in ammo:
			if ammoo.collides_with(player):
				log_event("ammo_pickup")
				ammo_pickup_sound = pygame.mixer.Sound("assets/ammo_pickup.wav")
				ammo_pickup_sound.set_volume(0.5)
				ammo_pickup_sound.play()
				player.gun_ammo += 100
				ammoo.kill()
		screen.fill("black")
		for item in drawable:
			item.draw(screen)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
		pygame.display.flip()
		dt = clock.tick(60) / 1000
#		print(f"{dt}")
if __name__ == "__main__":
    main()
