import pygame
import sys
import random
from player import Player
from collectibles import Collectible
from obstacles import Obstacle

pygame.init()

# settings
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
FPS = 60
SCROLL_SPEED = 5

# Perspective road 
ROAD_WIDTH_BOTTOM = SCREEN_WIDTH * 0.7
ROAD_WIDTH_TOP = SCREEN_WIDTH * 0.05
HORIZON = SCREEN_HEIGHT // 2 - 35
ROAD_HEIGHT = SCREEN_HEIGHT - HORIZON 

# colors
SKY_BLUE = (135, 206, 235)
RED = (255, 50, 50)
DARK_RED = (150, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 220, 0)
BLACK = (0, 0, 0)
BLUE = (3, 252, 223)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Run for Your GPA - 3D Road")
clock = pygame.time.Clock()

#assets
road_texture = pygame.image.load("assets/road3.png").convert_alpha()
map_w, map_h = road_texture.get_size()

sky_img = pygame.image.load("assets/sky.png").convert_alpha()
bg_img = pygame.image.load("assets/bg2.png").convert_alpha()
play_button_img = pygame.image.load("assets/start_button.png").convert_alpha()
gameover_img = pygame.image.load("assets/gameover.png").convert_alpha()
timesup_img = pygame.image.load("assets/times_up.png").convert_alpha()
border_img = pygame.image.load("assets/border.png").convert_alpha()


#player
player = Player((SCREEN_WIDTH // 2, SCREEN_HEIGHT - 130))

# object img
coin_img = pygame.image.load("assets/coin_2d.png").convert_alpha()
book_img = pygame.image.load("assets/book2_2d.png").convert_alpha()
cone_img = pygame.image.load("assets/cone2_2d.png").convert_alpha()
rock_img = pygame.image.load("assets/rock2_2d.png").convert_alpha()
popbus_img = pygame.image.load("assets/popbus_2d.png").convert_alpha()
work_img = pygame.image.load("assets/work_2d.png").convert_alpha()

nerd_img = pygame.image.load("assets/nerd.png").convert_alpha()
speed_img = pygame.image.load("assets/book.png").convert_alpha()
x2icon_img = pygame.image.load("assets/icon.png").convert_alpha()

collectible_images = [coin_img, book_img, nerd_img, work_img, speed_img]
obstacle_images = [cone_img, rock_img , popbus_img]

#fonts
font = pygame.font.Font("assets/ByteBounce.ttf", 45)
scoreFont = pygame.font.Font("assets/ByteBounce.ttf", 60)
GOfont = pygame.font.Font("assets/ByteBounce.ttf", 60)
title_font = pygame.font.Font("assets/ByteBounce.ttf", 80)
ThaiFont = pygame.font.Font("assets/TAGameboy-Regular.ttf", 45)


class Button:
    def __init__(self, center_pos, image):
        self.image = image
        self.rect = self.image.get_rect(center=center_pos)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        surface.blit(self.image, self.rect)
        return action

#draw perspective road
def draw_road(surface, scroll):
    road_view = pygame.Surface((SCREEN_WIDTH, ROAD_HEIGHT), pygame.SRCALPHA)
    for y in range(ROAD_HEIGHT):
        map_y = int(((scroll + (y / ROAD_HEIGHT) * map_h)) % map_h)
        src_line = road_texture.subsurface((0, map_y, map_w, 1))
        scale = y / ROAD_HEIGHT
        line_width = ROAD_WIDTH_TOP + (ROAD_WIDTH_BOTTOM - ROAD_WIDTH_TOP) * scale
        x_pos = SCREEN_WIDTH / 2 - line_width
        dest_width = int(line_width * 2)
        scaled_line = pygame.transform.scale(src_line, (dest_width, 2))
        road_view.blit(scaled_line, (x_pos, y))
    surface.blit(road_view, (0, HORIZON))

#main menu
def show_main_menu():
    start_button = Button((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60), play_button_img)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        #TITLE SCREEN (Change)
        screen.fill(SKY_BLUE)
        title_text = title_font.render("Run for Your GPA", True, WHITE)
        subtitle_text = font.render("Click Start to begin", True, WHITE)

        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3 - 70))
        screen.blit(subtitle_text, (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, SCREEN_HEIGHT // 3 + 20))

        #show button
        if start_button.draw(screen):
            return True

        pygame.display.flip()
        clock.tick(FPS)

def show_end():
    retry_button = Button((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60), play_button_img)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        screen.fill(BLACK)
        retry_text = title_font.render("TRY AGAIN?",True,WHITE)
        screen.blit(retry_text, (SCREEN_WIDTH//2-150, SCREEN_HEIGHT//2-100))

        if retry_button.draw(screen):
            return True

        pygame.display.flip()
        clock.tick(FPS)


#game start
def run_game():
    player = Player((SCREEN_WIDTH // 2, SCREEN_HEIGHT - 130))
    collectibles = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    scroll = 0
    spawn_timer = 60
    score = 0
    health = 100
    game_time = 60.0
    #buff variables
    multi = 1
    buff_timer = 0.0
    nerd_active = False
    speed_timer = 0.0
    speed_active = False

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        game_time = max(0.0, game_time - dt)

        keys = pygame.key.get_pressed()
        player.move(keys, dt) #from player.py

        scroll = (scroll - SCROLL_SPEED) % map_h

        screen.fill(SKY_BLUE)
        screen.blit(sky_img, (0, 0))
        screen.blit(bg_img, (0, 0))
        pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT // 71, SCREEN_WIDTH, SCREEN_HEIGHT // 14))

        draw_road(screen, scroll)

        #fix on track
        player_radius = 20
        road_left = max(player_radius, SCREEN_WIDTH / 2 - ROAD_WIDTH_BOTTOM + player_radius)
        road_right = min(SCREEN_WIDTH - player_radius, SCREEN_WIDTH / 2 + ROAD_WIDTH_BOTTOM - player_radius)
        player.clamp(road_left, road_right)

        #object spawning
        spawn_timer -= 1
        if spawn_timer <= 0:
            if random.random() < 0.6: #random
                new_collectible = Collectible(SCREEN_WIDTH // 2, ROAD_WIDTH_BOTTOM, ROAD_WIDTH_TOP, collectible_images) #from collectables.py
                img_ref = getattr(new_collectible, "image_original", None)
                # despawn when have buff
                if (nerd_active and img_ref == nerd_img) or (speed_active and img_ref == speed_img):
                    new_collectible.kill()
                else:
                    collectibles.add(new_collectible)
            else:
                obstacles.add(Obstacle(SCREEN_WIDTH // 2, ROAD_WIDTH_BOTTOM, ROAD_WIDTH_TOP, obstacle_images))
            spawn_timer = random.randint(30, 50) #spawn every 30-50 frames

        collectibles.update()
        obstacles.update()

        #x2 buff
        if buff_timer > 0.0:
            buff_timer = max(0.0, buff_timer - dt)
            if buff_timer <= 0.0:
                multi = 1
                nerd_active = False
        
        #speed buff
        if speed_timer > 0.0:
            speed_timer = max(0.0, speed_timer - dt)
            if speed_timer <= 0.0:
                player.player_speed = 5
                speed_active = False

        #collectables
        for collect in pygame.sprite.spritecollide(player, collectibles, True):
            score += 1 * multi
            # If the collected item is the nerd image, activate 2x buff
            if getattr(collect, "image_original", None) == nerd_img:
                multi = 2
                buff_timer = 8.0
                nerd_active = True
                # Despawn other nerd_img
                for other in list(collectibles):
                    if getattr(other, "image_original", None) == nerd_img:
                        other.kill()

            #speed
            elif getattr(collect, "image_original", None) == speed_img:
                player.player_speed = 10
                speed_timer = 8.0
                speed_active = True
                # Despawn other speed_img
                for other in list(collectibles):
                    if getattr(other, "image_original", None) == speed_img:
                        other.kill()

            health = min(100, health + 5) #player health

        #obstacles
        for obs in pygame.sprite.spritecollide(player, obstacles, True):
            score -= 1
            health -= 15

        collectibles.draw(screen)
        obstacles.draw(screen)
        player.draw(screen)

        #scores
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (20, 20))
        time_text = font.render(f"Time Left: {int(game_time)}", True, BLACK)
        screen.blit(time_text, (600, 20))

        #x2 buff
        if multi > 1:
            buff_count = scoreFont.render(f"Buff : {int(buff_timer)}",True, RED)
            screen.blit(x2icon_img,(25,100))
            screen.blit(buff_count,(115,120))
            pygame.draw.rect(screen, [255, 0, 0], [0, 0, 1000, 700], 1)

        #speed buff
        if player.player_speed > 5:
            speed_count = scoreFont.render(f"Speed : {int(speed_timer)}",True, BLUE)
            screen.blit(speed_count,(125,200))
            pygame.draw.rect(screen, SKY_BLUE , [0, 0, 1000, 700], 1)

        #health bar
        health_pos = 27
        health_text = font.render("Health : ", True, BLACK)
        screen.blit(health_text, (200, 20))
        bar_w = 200
        bar_h = 20
        pygame.draw.rect(screen, DARK_RED, (350, health_pos, bar_w, bar_h))
        pygame.draw.rect(screen, GREEN, (350, health_pos, int(bar_w * (health / 100)), bar_h))
        pygame.draw.rect(screen, WHITE, (350, health_pos, bar_w, bar_h), 2)

        #dies
        if health <= 0:
            img_width, img_height = gameover_img.get_size()
            x_pos = (SCREEN_WIDTH // 2) - (img_width // 2)
            y_pos = (SCREEN_HEIGHT // 2) - (img_height // 2)
            #screen.fill(SKY_BLUE)
            #screen.blit(gameover_img, (x_pos, y_pos))
            pygame.display.flip()
            return show_end()
            

        #times up
        if game_time <= 0:
            img_width, img_height = timesup_img.get_size()
            x_pos = (SCREEN_WIDTH // 2) - (img_width // 2)
            y_pos = (SCREEN_HEIGHT // 2) - (img_height // 2)
            screen.fill(SKY_BLUE)
            screen.blit(timesup_img, (x_pos, y_pos))
            score_display = scoreFont.render(f"Final Score: {score}", True, WHITE)
            screen.blit(score_display, ((SCREEN_WIDTH // 2) - 150, (SCREEN_HEIGHT // 2) + 75))
            pygame.display.flip()
            return show_end()
            

        pygame.display.flip()

    return True


def main():
    while True:
        start_requested = show_main_menu() 
        if not start_requested:
            break

        continue_running = run_game()
        if not continue_running:
            break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()