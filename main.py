import pygame
import sys
import random
import math
from player import Player
from objects import Objects

pygame.init()
pygame.mixer.init()

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
BLUE = (3, 107, 252)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Run for Your GPA - 3D Road")
clock = pygame.time.Clock()

#assets
road_texture = pygame.image.load("assets/road4.png").convert_alpha()
map_w, map_h = road_texture.get_size()

sky_img = pygame.image.load("assets/sky.png").convert_alpha()
bg_img = pygame.image.load("assets/bg2.png").convert_alpha()
play_button_img = pygame.image.load("assets/start_button.png").convert_alpha()
gameover_img = pygame.image.load("assets/gameover.png").convert_alpha()
timesup_img = pygame.image.load("assets/times_up.png").convert_alpha()
border_img = pygame.image.load("assets/border.png").convert_alpha()
cover_game_img = pygame.image.load("assets/cover_game.png").convert_alpha()
player_dei_img = pygame.image.load("assets/player_dei.png").convert_alpha()


#player
player = Player((SCREEN_WIDTH // 2, SCREEN_HEIGHT - 130))

# object img
coin_img = pygame.image.load("assets/coin_2d.png").convert_alpha()
book_img = pygame.image.load("assets/book2_2d.png").convert_alpha()
cone_img = pygame.image.load("assets/cone2_2d.png").convert_alpha()
rock_img = pygame.image.load("assets/rock2_2d.png").convert_alpha()
popbus_img = pygame.image.load("assets/big_popbus2.png").convert_alpha()
work_img = pygame.image.load("assets/work_2d.png").convert_alpha()
gradeA_img = pygame.image.load("assets/grade_A.png").convert_alpha()
gradeF_img = pygame.image.load("assets/grade_F.png").convert_alpha()
exam_img = pygame.image.load("assets/exam_2d.png").convert_alpha()


nerd_img = pygame.image.load("assets/nerd.png").convert_alpha()
speed_img = pygame.image.load("assets/run.png").convert_alpha()
shield_img = pygame.image.load("assets/turtle_shield.png").convert_alpha()
x2icon_img = pygame.image.load("assets/icon.png").convert_alpha()
speedicon_img = pygame.image.load("assets/speedicon.png").convert_alpha()
shieldicon_img = pygame.image.load("assets/turtle_shield.png").convert_alpha()

collectible_images = [coin_img, book_img, nerd_img, work_img, speed_img, shield_img, gradeA_img, exam_img]
obstacle_images = [cone_img, rock_img , popbus_img , gradeF_img]

#fonts
font = pygame.font.Font("assets/ByteBounce.ttf", 45)
scoreFont = pygame.font.Font("assets/ByteBounce.ttf", 60)
GOfont = pygame.font.Font("assets/ByteBounce.ttf", 60)
title_font = pygame.font.Font("assets/ByteBounce.ttf", 80)
ThaiFont = pygame.font.Font("assets/TAGameboy-Regular.ttf", 45)
pixel_font = pygame.font.Font("assets/PixelifySans-VariableFont_wght.ttf", 60)

#sfx
ding_sfx = pygame.mixer.Sound("SFX/ding2.mp3")
hit_sfx = pygame.mixer.Sound("SFX/hit.mp3")
lose_sfx = pygame.mixer.Sound("SFX/lose.mp3")
block_sfx = pygame.mixer.Sound("SFX/block.mp3")



class Button:
    def __init__(self, center_pos, image):
        self.image = image
        self.rect = self.image.get_rect(center=center_pos)
        self.clicked = False

    def draw(self, surface):
        action = False
        if pygame.mouse.get_pressed()[0] and not self.clicked:
            self.clicked = True
            action = True
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        offset_y = 15 * math.sin(2 * math.pi * 0.5 * (pygame.time.get_ticks() / 1000.0)) #moving button

        surface.blit(self.image, self.rect.move(0, offset_y))
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
    #asset is too big . scale down
    scaled_button = pygame.transform.scale(play_button_img, (int(play_button_img.get_width() * 0.8), int(play_button_img.get_height() * 0.8)))
    start_button = Button((SCREEN_WIDTH//2, 560), scaled_button)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        #TITLE SCREEN   
        img_width, img_height = cover_game_img.get_size()
        scale_factor = min(SCREEN_WIDTH / img_width, SCREEN_HEIGHT / img_height)
        scaled_width = int(img_width * scale_factor)
        scaled_height = int(img_height * scale_factor)
        scaled_img = pygame.transform.scale(cover_game_img, (scaled_width, scaled_height))
        x = (SCREEN_WIDTH - scaled_width) // 2
        y = (SCREEN_HEIGHT - scaled_height) // 2
        screen.blit(scaled_img, (x, y))

        #show button
        if start_button.draw(screen):
            return True

        pygame.display.flip()
        clock.tick(FPS)

def show_end(score): #end screen
    retry_button = Button((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200), play_button_img)
    lose_sfx.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        screen.fill(BLACK)
        score_display = scoreFont.render(f"Final Score: {score}", True, WHITE)
        screen.blit(score_display, ((SCREEN_WIDTH // 2) - 150, (SCREEN_HEIGHT // 2) - 300))
        retry_text = title_font.render("TRY AGAIN?",True,WHITE)
        screen.blit(retry_text, (SCREEN_WIDTH//2-160, SCREEN_HEIGHT//2-250))
        player_dei_scaled = pygame.transform.scale(player_dei_img, (300, 300)) #scale assets
        player_rect = player_dei_scaled.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)) #get pos
        screen.blit(player_dei_scaled, player_rect)

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
    shieldStatus = False

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0 # change to game second

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        game_time = max(0.0, game_time - dt) 

        keys = pygame.key.get_pressed() #get keys
        player.move(keys, dt) #from player.py move player

        scroll = (scroll - SCROLL_SPEED) % map_h

        screen.blit(sky_img, (0, 0))
        screen.blit(bg_img, (0, 0))
        pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT // 71, SCREEN_WIDTH, SCREEN_HEIGHT // 14))

        draw_road(screen, scroll)


        #fix on track
        player_radius = 300
        road_left = max(player_radius, SCREEN_WIDTH/2 - ROAD_WIDTH_BOTTOM + player_radius)
        road_right = min(SCREEN_WIDTH - player_radius, SCREEN_WIDTH / 2 + ROAD_WIDTH_BOTTOM - player_radius)
        player.clamp(road_left, road_right)

        #object spawning
        spawn_timer -= 1
        if spawn_timer <= 0:
            if random.random() < 0.6: #random
                new_collectible = Objects(SCREEN_WIDTH // 2, ROAD_WIDTH_BOTTOM, ROAD_WIDTH_TOP, collectible_images) #spawn object
                img_ref = getattr(new_collectible, "image_original", None) #check for images
                # despawn when have buff
                if (nerd_active and img_ref == nerd_img) or (speed_active and img_ref == speed_img) or (shieldStatus and img_ref == shield_img):
                    new_collectible.kill()
                else:
                    collectibles.add(new_collectible) #else add to pygame group
            else: # if not collectable. it is obstacle
                obstacles.add(Objects(SCREEN_WIDTH // 2, ROAD_WIDTH_BOTTOM, ROAD_WIDTH_TOP, obstacle_images)) #spawn object
            spawn_timer = random.randint(30, 50) #spawn every 30-50 frames

        collectibles.update()
        obstacles.update()

        #x2 buff
        if buff_timer > 0.0:
            buff_timer = max(0.0, buff_timer - dt) #never below 0
            if buff_timer <= 0.0:
                multi = 1
                nerd_active = False
        
        #speed buff
        if speed_timer > 0.0:
            speed_timer = max(0.0, speed_timer - dt)
            if speed_timer <= 0.0:
                player.player_speed = 5
                speed_active = False

        good_text = font.render("+SCORE",True,GREEN)
        bad_text = font.render("-SCORE",True,RED)

        #collectables
        for collect in pygame.sprite.spritecollide(player, collectibles, True):
            ding_sfx.play()
            score += 1 * multi
            # If the collected item is the nerd image, activate 2x buff
            if getattr(collect, "image_original", None) == nerd_img: #image_original is from objects.py . it sprite source image from collectabel list
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

            #shield
            elif getattr(collect, "image_original", None) == shield_img:
                shieldStatus = True
                # Despawn other speed_img
                for other in list(collectibles):
                    if getattr(other, "image_original", None) == shield_img:
                        other.kill()
            
            health = min(100, health + 5) #player health
            screen.blit(good_text,(SCREEN_WIDTH//2+350,20))

        #obstacles
        for obs in pygame.sprite.spritecollide(player, obstacles, True):
            hit_sfx.play()
            if shieldStatus==True:
                block_sfx.play()
                score = score
                health = health
                shieldStatus = False
            else:
                score = max(0, score - 1) #prevent score negative
                health -= 15 
            screen.blit(bad_text,(SCREEN_WIDTH//2+350,20))

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
            buff_count = scoreFont.render(f"x2: {int(buff_timer)}",True, RED)
            screen.blit(x2icon_img,(25,100))
            screen.blit(buff_count,(125,125))
            pygame.draw.rect(screen, [255, 0, 0], [0, 0, 1000, 700], 1)

        #speed buff
        if player.player_speed > 5:
            speed_count = scoreFont.render(f"Speed: {int(speed_timer)}",True, BLUE)
            screen.blit(speedicon_img,(25,210))
            screen.blit(speed_count,(125,235))
            pygame.draw.rect(screen, SKY_BLUE , [0, 0, 1000, 700], 1)
        
        #shield
        if shieldStatus == True:
            shield_text = scoreFont.render("Shield On!",True, BLACK)
            screen.blit(shieldicon_img,(350,115))
            screen.blit(shield_text,(420,120))

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
            pygame.display.flip()
            return show_end(score)
            

        #times up
        if game_time <= 0:
            pygame.display.flip()
            return show_end(score)
            

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
