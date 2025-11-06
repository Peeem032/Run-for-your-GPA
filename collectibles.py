import pygame
import random

# Constants for perspective motion
MAX_DEPTH = 1.0
MIN_DEPTH = 0.05   # The closest visible depth before disappearing
SPEED = 0.01       # How fast the collectible moves toward the camera

class Collectible(pygame.sprite.Sprite):
    def __init__(self, road_center, road_width_bottom, road_width_top, images):
        super().__init__()
        # Choose a random collectible image (e.g., coin or book)
        self.image_original = random.choice(images)

        # Road perspective data
        self.road_center = road_center
        self.road_width_bottom = road_width_bottom
        self.road_width_top = road_width_top

        # Start far away in the distance
        self.depth = MAX_DEPTH
        # Random horizontal offset along the road
        self.offset_x = random.uniform(-0.8, 0.8)

    def update(self):
        # Move closer each frame
        self.depth -= SPEED
        if self.depth < MIN_DEPTH:
            self.kill()
            return

        # Scale the sprite size according to its depth (perspective)
        scale = (1 - self.depth) * 2.5 + 0.2
        size = int(30 * scale)
        if size < 1:
            size = 1
        self.image = pygame.transform.scale(self.image_original, (size, size))

        # Compute screen position according to the perspective road shape
        road_half_width = (self.road_width_top + (self.road_width_bottom - self.road_width_top) * (1 - self.depth)) / 2
        screen_x = self.road_center + self.offset_x * road_half_width
        screen_y = 350 + (1 - self.depth) * 350  # Vertical movement along road depth

        self.rect = self.image.get_rect(center=(screen_x, screen_y))