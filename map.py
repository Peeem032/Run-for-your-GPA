import pygame
import random
from pytmx.util_pygame import load_pygame

# --- CONSTANTS ---
LANES = [-80, 0, 80]         # 3 horizontal lanes: left, center, right
SPEED = 8                    # Base movement speed for world scroll
ROAD_CENTER = 400            # Center position of the road on screen
ROAD_WIDTH_BOTTOM = 420      # Used for perspective width calculation


class Map:
    def __init__(self, tmx_path):
        # Load the TMX map file from Tiled
        self.tmx_data = load_pygame(tmx_path)
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight

        # --- Render the entire TMX map onto one Surface ---
        self.map_surface = pygame.Surface((self.width, self.height))
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, image in layer.tiles():
                    self.map_surface.blit(
                        image,
                        (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight)
                    )

        # Initial scroll offset (used for road animation)
        self.scroll_y = 0
        self.score = 0

        # --- Entities on the road ---
        # Collectibles (coins/books) positioned at random lanes and depths
        self.collectibles = [
            {
                "lane": random.choice(LANES),
                "depth": i * 400 + 800,  # Distance from camera
                "color": random.choice([(255, 80, 80), (80, 120, 255), (0, 230, 0)])  # Visual color
            }
            for i in range(12)
        ]

        # Obstacles (cones/rocks) placed at random distances
        self.obstacles = [
            {"lane": random.choice(LANES), "depth": i * 800 + 1000}
            for i in range(8)
        ]

    # Update world entities (scroll, collisions, reset objects)
    def update_world(self, player_x, dt):
        for c in self.collectibles:
            c["depth"] -= SPEED  # Move closer to player
            if c["depth"] < 100:
                # Collision check: compare player's x with collectible lane position
                if abs(player_x - (ROAD_CENTER + c["lane"])) < 48:
                    self.score += 1  # Player collected it
                # Respawn collectible further down the road
                c["depth"] = random.randint(3000, 5000)
                c["lane"] = random.choice(LANES)

        for o in self.obstacles:
            o["depth"] -= SPEED
            if o["depth"] < 100:
                # Collision check with obstacle
                if abs(player_x - (ROAD_CENTER + o["lane"])) < 48:
                    self.score = max(0, self.score - 3)  # Lose points
                # Respawn obstacle far away again
                o["depth"] = random.randint(4000, 7000)
                o["lane"] = random.choice(LANES)

        # Scroll background vertically (simulate road motion)
        self.scroll_y += SPEED * 8 * dt
        if self.scroll_y >= self.height:
            self.scroll_y = 0

        return self.score

    # Draw the TMX map with a pseudo-3D perspective effect
    def draw_perspective(self, surface):
        """Draws the .tmx map line by line to simulate 3D perspective."""
        screen_w, screen_h = surface.get_size()
        src_h = self.map_surface.get_height()
        scroll = int(self.scroll_y % src_h)

        for y in range(screen_h):
            # Scale factor: lower lines (bottom of screen) are stretched wider
            scale = 1.0 + (y / screen_h) * 2.0
            src_y = int((scroll + y) % src_h)

            # Extract one horizontal line (1 pixel tall) from map
            row = pygame.Surface((self.width, 1))
            row.blit(self.map_surface, (0, 0), (0, src_y, self.width, 1))

            # Scale it horizontally to create the perspective illusion
            scaled_row = pygame.transform.scale(row, (int(screen_w * scale), 1))
            x_offset = (screen_w - scaled_row.get_width()) // 2

            # Draw the scaled line on the screen
            surface.blit(scaled_row, (x_offset, y))

    # Draw collectibles and obstacles in perspective space
    def draw_entities(self, surface):
        # Draw collectibles as colored circles
        for c in self.collectibles:
            depth_scale = 1 / (c["depth"] / 800 + 1)  # Perspective scaling
            x = ROAD_CENTER + c["lane"] * depth_scale
            y = 600 - (c["depth"] * depth_scale)
            size = int(30 * depth_scale)
            pygame.draw.circle(surface, c["color"], (int(x), int(y)), size)

        # Draw obstacles as red rectangles
        for o in self.obstacles:
            depth_scale = 1 / (o["depth"] / 800 + 1)
            x = ROAD_CENTER + o["lane"] * depth_scale
            y = 600 - (o["depth"] * depth_scale)
            size = int(50 * depth_scale)
            pygame.draw.rect(surface, (200, 0, 0),
                             (x - size // 2, y - size // 2, size, size))