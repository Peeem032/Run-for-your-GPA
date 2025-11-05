import pygame
import pytmx
import sys
import random
from player import Player
from collectibles import Collectible
from obstacles import Obstacle

pygame.init()

# --- SETTINGS ---
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
FPS = 60
SCROLL_SPEED = 5

# Perspective road width
ROAD_WIDTH_BOTTOM = SCREEN_WIDTH * 0.25
ROAD_WIDTH_TOP = SCREEN_WIDTH * 0.05
HORIZON = SCREEN_HEIGHT // 2
ROAD_HEIGHT = SCREEN_HEIGHT - HORIZON

# --- COLORS ---
SKY_BLUE = (135, 206, 235)
GRASS_GREEN = (60, 179, 113)
RED = (255, 50, 50)
DARK_RED = (150, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 220, 0)

# --- INIT WINDOW ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Run for Your GPA - 3D Road")
clock = pygame.time.Clock()

# --- LOAD TMX MAP AS ROAD TEXTURE ---
# This creates a long road background image from a Tiled .tmx file
tmx_data = pytmx.util_pygame.load_pygame("Map/new_map_2.tmx")
tile_w, tile_h = tmx_data.tilewidth, tmx_data.tileheight
map_w, map_h = tmx_data.width * tile_w, tmx_data.height * tile_h

road_texture = pygame.Surface((map_w, map_h), pygame.SRCALPHA)
for y in range(tmx_data.height):
    for x in range(tmx_data.width):
        img = tmx_data.get_tile_image(x, y, 0)
        if img:
            road_texture.blit(img, (x * tile_w, y * tile_h))

# --- LOAD PLAYER ---
player = Player((SCREEN_WIDTH // 2, SCREEN_HEIGHT - 130))

# --- LOAD OBJECT IMAGES ---
# Load collectible and obstacle graphics
coin_img = pygame.image.load("assets/coin.png").convert_alpha()
book_img = pygame.image.load("assets/book.png").convert_alpha()
cone_img = pygame.image.load("assets/cone.png").convert_alpha()
rock_img = pygame.image.load("assets/rock.png").convert_alpha()

collectible_images = [coin_img, book_img]
obstacle_images = [cone_img, rock_img]

# --- SPRITE GROUPS ---
collectibles = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

# --- GAME VARIABLES ---
scroll = 0
spawn_timer = 60
score = 0
health = 100  # Player’s HP (health bar)
font = pygame.font.Font(None, 36)
running = True

# --- MAIN GAME LOOP ---
while running:
    dt = clock.tick(FPS) / 1000.0

    # --- EVENT HANDLING ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- PLAYER MOVEMENT ---
    keys = pygame.key.get_pressed()
    player.move(keys, dt)

    # --- SCROLLING ROAD ---
    scroll -= SCROLL_SPEED
    if scroll < 0:
        scroll = map_h

    # --- DRAW SKY AND GRASS ---
    screen.fill(SKY_BLUE)
    pygame.draw.rect(screen, GRASS_GREEN, (0, HORIZON, SCREEN_WIDTH, SCREEN_HEIGHT - HORIZON))

    # --- DRAW PERSPECTIVE ROAD ---
    road_view = pygame.Surface((SCREEN_WIDTH, ROAD_HEIGHT), pygame.SRCALPHA)
    for y in range(ROAD_HEIGHT):
        map_y = int((map_h - (scroll + (y / ROAD_HEIGHT) * map_h)) % map_h)
        src_line = road_texture.subsurface((0, map_y, map_w, 1))
        scale = y / ROAD_HEIGHT
        line_width = ROAD_WIDTH_TOP + (ROAD_WIDTH_BOTTOM - ROAD_WIDTH_TOP) * scale
        x_pos = SCREEN_WIDTH / 2 - line_width
        dest_width = int(line_width * 2)
        scaled_line = pygame.transform.scale(src_line, (dest_width, 2))
        road_view.blit(scaled_line, (x_pos, y))
    screen.blit(road_view, (0, HORIZON))

    # --- ROAD BOUNDARIES ---
    # Keep the player inside the visible road area
    road_left = SCREEN_WIDTH / 2 - ROAD_WIDTH_BOTTOM + 30
    road_right = SCREEN_WIDTH / 2 + ROAD_WIDTH_BOTTOM - 30
    player.clamp(road_left, road_right)

    # --- SPAWN OBJECTS ---
    spawn_timer -= 1
    if spawn_timer <= 0:
        if random.random() < 0.6:
            collectibles.add(Collectible(SCREEN_WIDTH // 2, ROAD_WIDTH_BOTTOM, ROAD_WIDTH_TOP, collectible_images))
        else:
            obstacles.add(Obstacle(SCREEN_WIDTH // 2, ROAD_WIDTH_BOTTOM, ROAD_WIDTH_TOP, obstacle_images))
        spawn_timer = random.randint(40, 80)

    # --- UPDATE OBJECTS ---
    collectibles.update()
    obstacles.update()

    # --- COLLISIONS ---
    for c in pygame.sprite.spritecollide(player, collectibles, True):
        score += 1
        health = min(100, health + 5)  # Gain small HP when collecting items
        print(f"💎 Collected item! Score: {score}, HP: {health}")

    for o in pygame.sprite.spritecollide(player, obstacles, True):
        score -= 1
        health -= 15  # Lose HP when hitting obstacles
        print(f"💥 Hit obstacle! Score: {score}, HP: {health}")

    # --- DRAW OBJECTS ---
    collectibles.draw(screen)
    obstacles.draw(screen)

    # --- DRAW PLAYER ---
    player.draw(screen)

    # --- DRAW SCORE ---
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (20, 20))

    # --- DRAW HEALTH BAR ---
    bar_x, bar_y, bar_w, bar_h = 20, 60, 200, 20
    pygame.draw.rect(screen, DARK_RED, (bar_x, bar_y, bar_w, bar_h))  # Empty bar
    pygame.draw.rect(screen, GREEN, (bar_x, bar_y, int(bar_w * (health / 100)), bar_h))  # Filled bar
    pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_w, bar_h), 2)  # Border

    # --- GAME OVER CHECK ---
    if health <= 0:
        game_over_text = font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    # --- UPDATE DISPLAY ---
    pygame.display.flip()