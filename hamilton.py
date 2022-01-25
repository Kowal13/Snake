import parameters


class HamiltonMovement:
    def __init__(self):
        self.direction_list = []
        self.go_to_edge()

    def reset(self):
        self.direction_list = []
        self.go_to_edge()

    def go_to_edge(self):
        for i in range(int(parameters.WIDTH/2) - 1):
            self.direction_list.append((1, 0))

    def start_cycle(self):
        for i in range(int(parameters.HEIGHT/2)):
            self.direction_list.append((0, -1))

        self.direction_list.append((-1, 0))

        for i in range(int(parameters.HEIGHT/2)):
            for j in range(parameters.WIDTH - 2):
                self.direction_list.append((-1, 0))
            self.direction_list.append((0, 1))
            for j in range(parameters.WIDTH - 2):
                self.direction_list.append((1, 0))
            if i != int(parameters.HEIGHT/2) - 1:
                self.direction_list.append((0, 1))

        self.direction_list.append((1, 0))

        for i in range(int(parameters.HEIGHT/2) - 1):
            self.direction_list.append((0, -1))

    def get_direction(self, key_arrows, snake, apple):
        if len(self.direction_list) == 0:
            self.start_cycle()

        direction = self.direction_list[0]
        self.direction_list.pop(0)
        return direction
