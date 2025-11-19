import pygame

# Player constants
PLAYER_RADIUS = 20


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.run_frames = [
            pygame.image.load("./assets/player/run1.png").convert_alpha(),
            pygame.image.load("./assets/player/run2.png").convert_alpha(),
            pygame.image.load("./assets/player/run3.png").convert_alpha()
        ]

        self.run_frames = [
            pygame.transform.scale(img, (120, 120)) for img in self.run_frames
        ]

        self.current_frame = 0
        self.frame_timer = 0
        self.animation_speed = 0.2  

        self.image = self.run_frames[self.current_frame]
        self.rect = self.image.get_rect(center=pos)
        self.player_speed = 5

        # Store position as floats for smoother movement
        self.x = pos[0]
        self.y = pos[1]
        self.radius = PLAYER_RADIUS

    def move(self, keys, dt):
        move_x = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x -= self.player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x += self.player_speed

        self.x += move_x * dt * 60

    def clamp(self, left_bound, right_bound):
        self.x = max(left_bound, min(right_bound, self.x))

    def update_animation(self):
        self.frame_timer += self.animation_speed
        if self.frame_timer >= 1:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.run_frames)
            self.image = self.run_frames[self.current_frame]

    def draw(self, surface):
        self.update_animation()

        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
        surface.blit(self.image, self.rect)