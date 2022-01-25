import parameters
import random


class Apple:
    def __init__(self):
        self.location = (0, 0)
        self.place_food([(int(parameters.WIDTH / 2), int(parameters.HEIGHT / 2)), (int(parameters.WIDTH / 2) - 1, int(parameters.HEIGHT / 2)), (int(parameters.WIDTH / 2) - 2, int(parameters.HEIGHT / 2))])

    def place_food(self, snake_area):
        x = random.randint(0, (parameters.WIDTH - 1))
        y = random.randint(0, (parameters.HEIGHT - 1))
        self.location = (x, y)
        if (x, y) in snake_area:
            self.place_food(snake_area)

    def get_mask(self):
        return [(self.location[0], self.location[1], parameters.RED)]
