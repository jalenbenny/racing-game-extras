import pygame
import random
from utils import Chariot, ShieldPowerUp, SpeedBoostPowerUp, HealthPackPowerUp

WHITE, RED, BLUE = (255, 255, 255), (255, 0, 0), (0, 0, 255)

TRACK_DETAILS = { 
    "assets/colosseum_track.png": {
        "start": (500, 680),
        "finish": pygame.Rect(550, 150, 20, 90),
        "bounds": [pygame.Rect(850, 50, 750, 700)],
        "boundsLeft": [pygame.Rect(0, 50 , 250, 700)],
        "boundsTop": [pygame.Rect(80, 0, 750, 140)],
        "boundsBottom": [pygame.Rect(25, 775, 800, 50)]
    },
    "assets/greektracks.png": {
        "start": (500, 680),
        "finish": pygame.Rect(550, 150, 20, 90),
        "bounds": [pygame.Rect(800, 620, 300, 300)]
    },
    "assets/modern_track.png": {
        "start": (500, 680),
        "finish": pygame.Rect(550, 150, 20, 90),
        "bounds": [pygame.Rect(800, 620, 300, 300)]
    },
    "assets/ancient_greece.png": {
        "start": (600, 750),
        "finish": pygame.Rect(580, 50, 100, 20),
        "bounds": [pygame.Rect(800, 150, 700, 500)]
    }
}

class RaceScreen:
    def __init__(self, screen, track_image_path):
        self.screen = screen
        self.track_img = pygame.image.load(track_image_path)
        self.track_img = pygame.transform.scale(self.track_img, (1100, 850))

        self.track_data = TRACK_DETAILS[track_image_path]
        self.player = Chariot(*self.track_data["start"])  # Spawn at track's start position
        self.finish_zone = self.track_data["finish"]
        self.track_bounds = self.track_data["bounds"]

        # Power-ups setup: Shield, Speed Boost, and Health Pack
        self.powerups = []
        for _ in range(2):  # spawn two of each type
            self.powerups.append(ShieldPowerUp(random.randint(100, 900), random.randint(100, 700)))
            self.powerups.append(SpeedBoostPowerUp(random.randint(100, 900), random.randint(100, 700)))
            self.powerups.append(HealthPackPowerUp(random.randint(100, 900), random.randint(100, 700)))

        # Exit Button
        self.exit_button = pygame.Rect(20, 720, 150, 50)
        self.font = pygame.font.Font(None, 36)

    def draw_exit_button(self):
        pygame.draw.rect(self.screen, RED, self.exit_button)
        text = self.font.render("Exit", True, WHITE)
        self.screen.blit(text, (self.exit_button.x + 50, self.exit_button.y + 10))

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            clock.tick(30)
            self.screen.fill(WHITE)
            self.screen.blit(self.track_img, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.exit_button.collidepoint(event.pos):
                        return "exit"  # Go back to home screen

            keys = pygame.key.get_pressed()
            self.player.move(keys)
            self.player.check_collision(self.track_bounds)

            # Power-ups collision handling
            for powerup in self.powerups[:]:  # copy of the list for safe removal
                if self.player.rect.colliderect(powerup.rect):
                    if isinstance(powerup, ShieldPowerUp):
                        self.player.activate_shield()
                        print("Picked up Shield Power-Up!")
                    elif isinstance(powerup, SpeedBoostPowerUp):
                        self.player.activate_boost()
                        print("Picked up Speed Boost Power-Up!")
                    elif isinstance(powerup, HealthPackPowerUp):
                        self.player.restore_health(20)
                        print("Picked up Health Pack Power-Up!")

                    # Remove power-up from the screen
                    self.powerups.remove(powerup)

            # Draw elements
            self.player.draw(self.screen)

            for powerup in self.powerups:
                powerup.draw(self.screen)

            # Draw Exit Button
            self.draw_exit_button()

            # Win / Lose Conditions
            if self.player.health <= 0:
                print("Game Over! You lost!")
                return "lose"

            if self.player.laps >= 2:
                print("Congratulations! You won!")
                return "win"

            if self.player.rect.colliderect(self.finish_zone):
                return "win"

            pygame.draw.rect(self.screen, (200, 0, 0), self.finish_zone)

            pygame.display.update()
