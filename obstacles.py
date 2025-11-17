import pygame
import random

# Constants for perspective scaling and motion
MAX_DEPTH = 1.0
MIN_DEPTH = 0.05
SPEED = 0.0075

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, road_center, road_width_bottom, road_width_top, images):
        super().__init__()
        # Choose a random obstacle image (e.g., cone or rock)
        self.image_original = random.choice(images)

        # Perspective parameters
        self.road_center = road_center
        self.road_width_bottom = road_width_bottom
        self.road_width_top = road_width_top

        # Start far away
        self.depth = MAX_DEPTH
        self.offset_x = random.uniform(-0.7, 0.7)

    def update(self):
        # Move closer to the player
        self.depth -= SPEED
        if self.depth < MIN_DEPTH:
            self.kill()
            return

        # Resize the obstacle as it approaches (perspective scaling)
        scale = (1 - self.depth) * 2.5 + 0.2
        size = int(40 * scale)
        if size < 1:
            size = 1
        self.image = pygame.transform.scale(self.image_original, (size, size))

        # Compute on-road perspective position
        road_half_width = (self.road_width_top + (self.road_width_bottom - self.road_width_top) * (1 - self.depth)) / 2
        screen_x = self.road_center + self.offset_x * road_half_width
        screen_y = 300 + (1 - self.depth) * 320
        self.rect = self.image.get_rect(center=(screen_x, screen_y))