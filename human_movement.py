import pygame.event


class HumanMovement:
    def __init__(self):
        self.direction = (1, 0)

    def reset(self):
        self.direction = (1, 0)

    def get_direction(self, key_arrows, snake=None, apple=None):
        direction = None
        right, left, up, down = key_arrows
        if right:
            direction = (1, 0)
        elif left:
            direction = (-1, 0)
        elif up:
            direction = (0, -1)
        elif down:
            direction = (0, 1)

        if direction is not None:
            self.direction = direction

        return self.direction
