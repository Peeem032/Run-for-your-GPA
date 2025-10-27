import pygame, sys
from setting import *

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)  # Init sprite and add to groups

        # Load player image and scale
        self.image = pygame.image.load("./assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (128, 128))

        # Get rect and set position
        self.rect = self.image.get_rect(center=pos)

        # Lanes x positions
        self.lanes_x = [190, 305, 420]
        self.current_lane = 1  # start middle
        self.move_speed = 400  # speed

        self.grounded_y = pos[1]  # y position (ground)
        self.alive = True  # is alive

    # Handle key press
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and self.current_lane < len(self.lanes_x) - 1:
                self.current_lane += 1  # move right
            elif event.key == pygame.K_LEFT and self.current_lane > 0:
                self.current_lane -= 1  # move left

    # Update player position
    def update(self, dt):
        if not self.alive:
            return  # stop if dead

        # Move to target lane
        target_x = self.lanes_x[self.current_lane]
        dx = target_x - self.rect.centerx

        if abs(dx) < 5:
            self.rect.centerx = target_x  # snap to lane
        else:
            self.rect.centerx += self.move_speed * dt * (1 if dx > 0 else -1)  # move smoothly