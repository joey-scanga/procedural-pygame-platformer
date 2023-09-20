import pygame
import pymunk
import pymunk.pygame_util
from maze import Maze
from game_objects import *
from config import *

def gen_floors(clusters=10):
    floors = []
    for _ in range(clusters):
        floor_maze = Maze(SCREEN_HEIGHT // FLOOR_TILE_SIZE, SCREEN_WIDTH // FLOOR_TILE_SIZE, length=100)
        for i in range(0, len(floor_maze.maze)):
            for j in range(0, len(floor_maze.maze[i])):
                if floor_maze.maze[i][j] == 1:
                    floors.append(Floor(j * FLOOR_TILE_SIZE, i * FLOOR_TILE_SIZE, FLOOR_TILE_SIZE, FLOOR_TILE_SIZE))
                elif floor_maze.maze[i][j] == 2:
                    floors.append(Launchpad(j * FLOOR_TILE_SIZE, i * FLOOR_TILE_SIZE, FLOOR_TILE_SIZE, FLOOR_TILE_SIZE))
    # for f in floors:
    #     bodies.append(pymunk.Body())
    #     vertices = [(f.x, f.y), (f.x + FLOOR_TILE_SIZE, f.y), \
    #             (f.x, f.y + FLOOR_TILE_SIZE), (f.x + FLOOR_TILE_SIZE, f.y + FLOOR_TILE_SIZE)]
    #     polys.append(pymunk.Poly(None, vertices))
        
    return floors

def gen_floor_physics(floors, space):
    w = h = FLOOR_TILE_SIZE
    for f in floors:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Poly.create_box(body, (w, h), 0.0)
        shape.position = f.rect.center
        space.add(body, shape)


        
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    
    global_physics_space= pymunk.Space()
    global_physics_space.damping = 0.9
    global_physics_space.gravity = (0, 10)
    floors = gen_floors()
    gen_floor_physics(floors, global_physics_space)
    test_player = Player(SCREEN_WIDTH // 2, 0)

    options = pymunk.pygame_util.DrawOptions(screen)

    obj_group = pygame.sprite.Group() 
    obj_group.add(test_player, *floors)

    while running:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            obj_group.remove(*floors)
            floors = gen_floors()
            obj_group.add(*floors)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        test_player.update(obj_group, [o for o in obj_group if isinstance(o, Floor)], global_physics_space)
        if test_player.rope:
            obj_group.add(test_player.rope)
            test_player.rope.update([o for o in obj_group if isinstance(o, Floor)])
            pygame.draw.line(screen, pygame.Color("brown"), test_player.rect.center, test_player.rope.rect.center, width=7)

        screen.fill("purple")
        global_physics_space.step(1)
     
        obj_group.draw(screen)



        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
