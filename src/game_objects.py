import pygame, time
import pymunk.constraints
from enum import Enum
from rope import Rope
from config import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=5, color=pygame.Color("green"), \
            width=10, height=10):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dir = {"left": 0, "right": 0} 
        self.speed = speed
        self.x_vel = 0
        self.y_vel = 0
        self.jumping = True
        self.rope = None
        self.swinging = False
        self.body = None
        self.rope_body = None
        self.rope_constraint = None


    def handle_input(self, obj_group):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self.rope = None
            self.rect.topleft = (SCREEN_WIDTH // 2, -20)
        
        if not self.rope:
            if keys[pygame.K_LEFT]:
                self.dir["left"] = 1
            else:
                self.dir["left"] = 0
            if keys[pygame.K_RIGHT]:
                self.dir["right"] = 1
            else:
                self.dir["right"] = 0

            self.x_vel = (-self.dir["left"] * self.speed)\
                    + (self.dir["right"] * self.speed)

        elif self.rope and self.body:
            if keys[pygame.K_LEFT]:
                self.body.apply_impulse_at_local_point((-50, 0))
            if keys[pygame.K_RIGHT]:
                self.body.apply_impulse_at_local_point((50, 0))
       
        if keys[pygame.K_w] and not self.rope:
            self.create_rope(180)
        if keys[pygame.K_q] and not self.rope:
            self.create_rope(225)
        if keys[pygame.K_e] and not self.rope:
            self.create_rope(135)
        if keys[pygame.K_UP] and self.rope:
            if self.rope_constraint:
                self.rope_constraint.distance -= 2
        if keys[pygame.K_DOWN] and self.rope:
            if self.rope_constraint:
                self.rope_constraint.distance += 2
        if keys[pygame.K_SPACE] and self.rope:
            obj_group.remove(self.rope)
            if self.body:
                self.x_vel = self.body.velocity.x * self.speed
                self.y_vel = self.body.velocity.y * self.speed
            self.rope = self.body = self.rope_body = self.rope_constraint = None
            self.swinging = False



        if keys[pygame.K_SPACE] and not self.jumping:
            self.y_vel = JUMP_VEL
            self.jumping = True

    def create_rope(self, angle):
        self.rope = Rope(self, angle)

    def transform_to_physics_object(self, space):
        self.body = pymunk.Body(10, 10)
        self.body.position = self.rect.center
        body_shape = pymunk.Circle(self.body, 5)
        body_shape.elasticity = 0.9
        body_shape.friction = 0.4
        body_shape.mass = 10
        space.add(self.body, body_shape)
        self.rope_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.rope_body.position = self.rope.rect.center
        rope_body_shape = pymunk.Circle(self.body, 5)
        rope_body_shape.elasticity = 0.9
        rope_body_shape.friction = 0.4
        rope_body_shape.mass = 10
        space.add(self.rope_body, rope_body_shape)
        self.rope_constraint = pymunk.constraints.PinJoint(self.body, \
                self.rope_body )
        space.add(self.rope_constraint)


    def handle_collision(self, possible_collision_rects):
        collidedtiles = self.rect.move(0, 1).collidelistall(possible_collision_rects)

        if not collidedtiles:
            self.jumping = True
            return

        for i in collidedtiles:
            axes = {
                'b': (pow(self.rect.midtop[0] - possible_collision_rects[i].rect.centerx, 2) + pow(self.rect.midtop[1] - possible_collision_rects[i].rect.centery, 2)),
                't': (pow(self.rect.midbottom[0] - possible_collision_rects[i].rect.centerx, 2) + pow(self.rect.midbottom[1] - possible_collision_rects[i].rect.centery, 2)),
                'r': (pow(self.rect.midleft[0] - possible_collision_rects[i].rect.centerx, 2) + pow(self.rect.midleft[1] - possible_collision_rects[i].rect.centery, 2)),
                'l': (pow(self.rect.midright[0] - possible_collision_rects[i].rect.centerx, 2) + pow(self.rect.midright[1] - possible_collision_rects[i].rect.centery, 2))
            }

            shallow_axis = min(axes, key=axes.get)
            
            if shallow_axis == 't' and isinstance(possible_collision_rects[i], Launchpad):
                self.y_vel = JUMP_VEL * 2
            elif shallow_axis == 't':
                self.rect.bottom = possible_collision_rects[i].rect.top - 1
                self.y_vel = 0
                self.jumping = False
            elif shallow_axis == 'b':
                self.rect.top = possible_collision_rects[i].rect.bottom + 1
                self.y_vel = 0
            elif shallow_axis == 'l':
                self.rect.right = possible_collision_rects[i].rect.left - 1
                self.x_vel = 0
            elif shallow_axis == 'r':
                self.rect.left = possible_collision_rects[i].rect.right + 1
                self.x_vel = 0

        
    def update(self, obj_group, possible_collision_rects, space):
        '''
        Handles input, updates player's x and y values.

        :param obj_group: pygame sprite group of current ingame objects
        :param possible_collision_rects: rectangles from obj_group that the player could collide with
        '''
        self.handle_input(obj_group)
        self.handle_collision(possible_collision_rects)

        if self.swinging:
            self.rect.center = (self.body.position.x, self.body.position.y)
            print(self.body.velocity.x)
            print(self.body.velocity.y)

        elif self.rope and self.rope.is_anchored and not self.swinging:
            self.transform_to_physics_object(space)
            self.swinging = True

        elif self.jumping:
            self.y_vel += GRAVITY
            if self.y_vel > 5:
                self.y_vel = 5

        if not self.swinging: 
            self.rect.y += self.y_vel
            self.rect.x += self.x_vel


       



class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=pygame.Color("blue")):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

class Launchpad(Floor):
    def __init__(self, x, y, width, height, color=pygame.Color("yellow")):
        super().__init__(x, y, width, height, color=color)








