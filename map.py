import pygame
from pytmx.util_pygame import load_pygame

class Map:
    def __init__(self, new_map_2):
        self.tmx_data = load_pygame("Map/new_map_2.tmx")
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight

        self.map_surface = pygame.Surface((self.width, self.height))
        self.render_map()

        self.scroll_y = 0

    def render_map(self):
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, image in layer.tiles():
                    self.map_surface.blit(image, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))
    
    def draw(self, surface, dt, scroll_speed):
        self.scroll_y += scroll_speed * dt
        if self.scroll_y >= self.height:
            self.scroll_y = 0

        surface.blit(self.map_surface, (0, self.scroll_y - self.height))
        surface.blit(self.map_surface, (0, self.scroll_y))