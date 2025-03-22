import pygame

WIDTH, HEIGHT = 1000, 800

class Chariot:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.speed = 5
        self.normal_speed = self.speed  # store base speed for boost reset
        self.image = pygame.image.load("assets/chariot.png")
        self.image = pygame.transform.scale(self.image, (60, 40))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 100
        self.shield_active = False
        self.shield_timer = 0
        self.boost_active = False
        self.boost_timer = 0
        self.laps = 0

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - 60:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - 40:
            self.y += self.speed
        self.rect.topleft = (self.x, self.y)

    def check_collision(self, track_bounds):
        for boundary in track_bounds:
            if self.rect.colliderect(boundary):
                self.health -= 0.5
                print(f"Collision! Health: {self.health}")

        # Check shield expiration
        if self.shield_active and pygame.time.get_ticks() - self.shield_timer > 6000:
            self.shield_active = False

        # Check boost expiration
        if self.boost_active and pygame.time.get_ticks() - self.boost_timer > 5000:
            self.boost_active = False
            self.speed = self.normal_speed

    def activate_shield(self):
        self.shield_active = True
        self.shield_timer = pygame.time.get_ticks()
        print("Shield Activated!")

    def activate_boost(self):
        self.boost_active = True
        self.boost_timer = pygame.time.get_ticks()
        self.speed = 9  # boost speed!
        print("Speed Boost Activated!")

    def restore_health(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100
        print(f"Health Restored! Health: {self.health}")

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        # health bar
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, self.health * 2, 20))


class ShieldPowerUp:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 0, 255))  # blue color for shield
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class SpeedBoostPowerUp:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 165, 0))  # orange color for speed boost
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class HealthPackPowerUp:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0))  # green color for health pack
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
