import param
import random


class Apple:
    def __init__(self):
        self.location = (0, 0)
        self.place_food([(int(param.WIDTH / 2), int(param.HEIGHT / 2)), (int(param.WIDTH / 2)-1, int(param.HEIGHT / 2)), (int(param.WIDTH / 2)-2, int(param.HEIGHT / 2))])

    def place_food(self, snake_area):
        x = random.randint(0, (param.WIDTH - 1))
        y = random.randint(0, (param.HEIGHT - 1))
        self.location = (x, y)
        if (x, y) in snake_area:
            self.place_food(snake_area)

    def get_mask(self):
        return [(self.location[0], self.location[1], param.RED)]
