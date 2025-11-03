import pygame, sys
import time
import random

from setting import *
from player import Player
from map import Map
from objects import Objects



class Game:
    def __init__(self):
        pygame.init()
        #create display game
        self.display_surface = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Run for Your GPA")
        self.clock = pygame.time.Clock()

        #load map
        self.map = Map("map/map.tmx")

        #create player
        self.all_sprites = pygame.sprite.Group()
        self.player = Player((300, 300), self.all_sprites)
        

        self.circles = pygame.sprite.Group()
        self.last_circle_spawn = time.time()
        self.circle_spawn_interval = 1.0  # seconds between spawns


        self.scroll_speed = 125
        
        #time
        self.start_time = time.time()
        self.limit_time = 10

        self.font = pygame.font.Font(None, 48)

        self.running = True

    #timer
    def update_timer(self):
        current_time = time.time() - self.start_time
        time_left = max(0, self.limit_time - current_time)
        return time_left
    
    #show time on display
    def draw_timer(self, time_left):
        time_text = self.font.render(f"Time: {int(time_left)}", True, (0, 0, 0))
        self.display_surface.blit(time_text, (10, 10))
    
    #main run game
    def run(self):
        #main loop game    
        while self.running:
            #frame rate 60 fps
            dt = self.clock.tick(60)/1000

            #manage event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                #send event to player
                self.player.handle_event(event)

            #update all sprites
            self.all_sprites.update(dt)
            self.circles.update(dt)

            #spawn circle
            current_time = time.time()
            if current_time - self.last_circle_spawn > self.circle_spawn_interval and self.player.alive:
                random_x = random.randint(190, 420)
                self.circle = Objects((random_x, 0))
                self.all_sprites.add(self.circle)
                self.last_circle_spawn = current_time

            #draw background
            self.display_surface.fill("white")
            self.map.draw(self.display_surface, dt, self.scroll_speed)

            #update time
            time_left = self.update_timer()
            self.draw_timer(time_left)

            #when time ends, close window/ return to menu
            if int(time_left)==0:
                self.display_surface.fill("white")
                End_text = self.font.render(f"GAME OVER", True, (0, 0, 0))
                self.display_surface.blit(End_text, (200, 200))
                self.player.alive = False
                
            

            #draw player
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()

                
    
        pygame.quit()
    
if __name__ == "__main__" :
    game = Game()
    game.run()
