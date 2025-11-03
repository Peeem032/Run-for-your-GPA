import pygame

class Objects(pygame.sprite.Sprite):
    def __init__(self, pos, radius=20, color=(255, 0, 0), speed=125):
        super().__init__()
        self.radius = radius
        self.color = color
        self.speed = speed
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=pos)

    def update(self, dt):
        self.rect.y += self.speed * dt
        