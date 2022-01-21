import param
import random


class Apple:
    def __init__(self):
        self.place_food([])

    def place_food(self, snake_area):
        x = random.randint(0, (param.WIDTH - 1))
        y = random.randint(0, (param.HEIGHT - 1))
        self.location = (x, y)

    def get_mask(self):
        return [(self.location[0], self.location[1], param.RED)]
