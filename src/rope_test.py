import pygame, random
from config import *
import pymunk as pm
import pymunk.pygame_util
from pymunk.vec2d import Vec2d

def main():
    #Hacks for converting pymunk to pygame coords
    def to_pygame(p):
        return int(p.x), int(-p.y + SCREEN_HEIGHT)

    def from_pygame(p):
        return to_pygame(p)

    def reset_bodies(space):
        for body in space.bodies:
            body.position = Vec2d(*body.start_position)
            body.force = 0, 0
            body.torque = 0
            body.velocity = 0, 0
            body.angular_velocity = 0
        color = pygame.Color("blue")
        for shape in space.shapes:
            shape.color = color

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    space = pymunk.Space()
    space.gravity = 0, -900
    space.damping = .999

    bodies = []
    
    #circle body
    mass = 10
    radius = 25
    moment = pm.moment_for_circle(mass, 0, radius, (0, 0))
    body = pm.Body(mass, moment)
    body.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    body.start_position = Vec2d(*body.position)
    shape = pm.Circle(body, radius)
    shape.elasticity = 0.99999
    space.add(body, shape)
    bodies.append(body)
    pj = pm.PinJoint(space.static_body, body, \
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200), (0, 0))
    space.add(pj)

    reset_bodies(space)
    selected = None

    pygame.time.set_timer(pygame.USEREVENT + 1, 70000)
    pygame.time.set_timer(pygame.USEREVENT + 2, 120000)
    pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT + 1:
                r = random.randint(1, 4)
                for body in bodies[0:r]:
                    body.apply_impulse_at_local_point((-6000, 0))

            if event.type == pygame.USEREVENT + 2:
                reset_bodies(space)


            elif event.type == pygame.KEYDOWN:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        screen.fill(pygame.Color("purple"))

        for c in space.constraints:
            pv1 = c.a.position + c.anchor_a
            pv2 = c.b.position + c.anchor_b
            p1 = to_pygame(pv1)
            p2 = to_pygame(pv2)
            pygame.draw.aalines(screen, pygame.Color("green"), False, [p1, p2])

        for ball in space.shapes:
            p = to_pygame(ball.body.position)
            pygame.draw.circle(screen, ball.color, p, int(ball.radius), 0)


        fps = 50
        iterations = 25
        dt = 1.0 / float(fps) / float(iterations)
        for x in range(iterations):
            space.step(dt)

        pygame.display.flip()
        clock.tick(fps)
            
            
if __name__ == "__main__":
    main()
