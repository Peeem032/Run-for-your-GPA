import pygame

# Player constants
PLAYER_RADIUS = 40
PLAYER_SPEED = 5

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # Load and scale player sprite
        self.image = pygame.image.load("./assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=pos)

        # Store position as floats for smoother movement
        self.x = pos[0]
        self.y = pos[1]
        self.radius = PLAYER_RADIUS

    def move(self, keys, dt):
        # Move left/right based on user input
        move_x = 0
        if keys[pygame.K_LEFT]:
            move_x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            move_x += PLAYER_SPEED
        self.x += move_x * dt * 60

    def clamp(self, left_bound, right_bound):
        # Keep player within the road boundaries
        self.x = max(left_bound, min(right_bound, self.x))

    def draw(self, surface):
        # Update sprite position and draw it
        self.rect.centerx = int(self.x)
        surface.blit(self.image, self.rect)