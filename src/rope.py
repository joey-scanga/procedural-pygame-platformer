import pygame, time, math
import pymunk
from config import *

class Rope(pygame.sprite.Sprite):
    def __init__(
            self, 
            player,
            angle,
            color=pygame.Color("brown")
            ):
        super().__init__()
        self.image = pygame.Surface((ROPE_WIDTH, ROPE_WIDTH))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=player.rect.center)
        self.angle = angle
        self.color = color
        self.extending = True
        self.is_anchored = False

    def handle_collision(self, obj_group):
        possible_collision_rects = [o for o in obj_group]

        collidedtiles = self.rect.collidelistall(possible_collision_rects)
        if not collidedtiles:
            return False

        for i in collidedtiles:
            axes = {
                'b': (pow(self.rect.midtop[0] - possible_collision_rects[i].rect.centerx, 2) + pow(self.rect.midtop[1] - possible_collision_rects[i].rect.centery, 2)),
                't': (pow(self.rect.midbottom[0] - possible_collision_rects[i].rect.centerx, 2) + pow(self.rect.midbottom[1] - possible_collision_rects[i].rect.centery, 2)),
                'r': (pow(self.rect.midleft[0] - possible_collision_rects[i].rect.centerx, 2) + pow(self.rect.midleft[1] - possible_collision_rects[i].rect.centery, 2)),
                'l': (pow(self.rect.midright[0] - possible_collision_rects[i].rect.centerx, 2) + pow(self.rect.midright[1] - possible_collision_rects[i].rect.centery, 2))
            }

            shallow_axis = min(axes, key=axes.get)
            
            if shallow_axis == 't':
                self.rect.bottom = possible_collision_rects[i].rect.top - 1
                self.y_vel = self.x_vel = 0
            if shallow_axis == 'b':
                self.rect.top = possible_collision_rects[i].rect.bottom + 1
                self.y_vel = self.x_vel = 0
            if shallow_axis == 'l':
                self.rect.right = possible_collision_rects[i].rect.left - 1
                self.y_vel = self.x_vel = 0
            if shallow_axis == 'r':
                self.rect.left = possible_collision_rects[i].rect.right + 1
                self.y_vel = self.x_vel = 0

        return True

    def update(self, obj_group):
        if self.extending:
            dy = math.cos((math.pi * 2 * self.angle / 360)) * ROPE_SPEED
            dx = math.sin((math.pi * 2 * self.angle / 360)) * ROPE_SPEED
            self.rect.x += int(dx)
            self.rect.y += int(dy)
            if self.handle_collision(obj_group):
                self.extending = False
        else:
            self.is_anchored = True
            
        
        

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    test_rope = Rope(30, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    rope_group = pygame.sprite.Group()
    rope_group.add(test_rope)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")
        test_rope.update()
        rope_group.draw()

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
     
