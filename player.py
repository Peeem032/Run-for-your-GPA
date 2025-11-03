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

         # Free movement settings
        self.move_speed = 300  #horizontal movement speed
        self.velocity_x = 0  #current horizontal velocity

        self.grounded_y = pos[1]  #y position (ground)
        self.alive = True  #is alive

        # Screen boundaries (adjust based on your player size)
        self.min_x = 150 #left boundary
        self.max_x = 460  #right boundary

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.velocity_x = self.move_speed  #move right
            elif event.key == pygame.K_LEFT:
                self.velocity_x = -self.move_speed  #move left
        
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                self.velocity_x = 0  #stop moving

    # Update player position
    def update(self, dt):
        if not self.alive:
            return  #stop if dead

        # Move horizontally based on velocity
        self.rect.centerx += self.velocity_x * dt

        # Keep player within screen boundaries
        if self.rect.centerx < self.min_x:
            self.rect.centerx = self.min_x
        elif self.rect.centerx > self.max_x:
            self.rect.centerx = self.max_x