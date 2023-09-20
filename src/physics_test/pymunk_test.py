import pymunk


if __name__ == "__main__":
    space = pymunk.Space()
    space.gravity = 0, -981

    body = pymunk.Body()
    body.position = 50, 100

    poly = pymunk.Poly.create_box(body)
    poly.mass = 10
    space.add(body, poly)

    print_options = pymunk.SpaceDebugDrawOptions()

    for _ in range(100):
        space.step(0.02)
        space.debug_draw(print_options)
