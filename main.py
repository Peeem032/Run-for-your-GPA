import pygame, sys
import time

from setting import *
from player import Player
from map import Map


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

        self.scroll_speed = 200
        
        #time
        self.start_time = time.time()
        self.limit_time = 20

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

            #draw background
            self.display_surface.fill("white")
            self.map.draw(self.display_surface, dt, self.scroll_speed)

            #update time
            time_left = self.update_timer()
            self.draw_timer(time_left)

            #draw player
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()

    
        pygame.quit()
    
if __name__ == "__main__" :
    game = Game()
    game.run()
