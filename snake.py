import parameters


class Snake:
    def __init__(self):
        self.head = (int(parameters.WIDTH / 2), int(parameters.HEIGHT / 2))  # (x , y)
        self.body = [(self.head[0] - 1, self.head[1]), (self.head[0] - 2, self.head[1])]

    def is_out_of_boundary(self, point=None):

        if point is None:
            point = self.head

        if point[0] > parameters.WIDTH - 1:
            return True

        elif point[0] < 0:
            return True

        elif point[1] > parameters.HEIGHT - 1:
            return True

        elif point[1] < 0:
            return True

        return False

    def is_collision(self, point=None):

        if point is None:
            point = self.head

        if point in self.body:
            return True

        return False

    def was_apple_eaten(self, apple_location):

        if self.head == apple_location:
            return True

        return False

    def get_mask(self):

        dark_green = self.head
        color_list = [(dark_green[0], dark_green[1], parameters.DARK_GREEN)]

        for el in self.body:
            color_list.append((el[0], el[1], parameters.GREEN))

        return color_list

    def move(self, direction, apple_location):
        # direction is a tuple
        # (1, 0) - right, (-1, 0) - left, (0, 1) - down, (0, -1) - up

        zipped = zip(self.head, direction)
        mapped = map(sum, zipped)
        new_head = tuple(mapped)
        self.body.insert(0, self.head)
        self.head = new_head

        if not self.was_apple_eaten(apple_location):
            self.body.pop()
