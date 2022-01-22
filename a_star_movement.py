import param
from random import randint


class Node:

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.previous = None
        self.obstacle = False

    def add_neighbors(self, grid, columns, rows):

        neighbor_x = self.x
        neighbor_y = self.y

        if neighbor_x < columns - 1:
            self.neighbors.append(grid[neighbor_x + 1][neighbor_y])
        if neighbor_x > 0:
            self.neighbors.append(grid[neighbor_x - 1][neighbor_y])
        if neighbor_y < rows - 1:
            self.neighbors.append(grid[neighbor_x][neighbor_y + 1])
        if neighbor_y > 0:
            self.neighbors.append(grid[neighbor_x][neighbor_y - 1])
        # diagonals
        """ if neighbor_x > 0 and neighbor_y > 0:
            self.neighbors.append(grid[neighbor_x-1][neighbor_y-1])
        if neighbor_x < columns -1 and neighbor_y > 0:
            self.neighbors.append(grid[neighbor_x+1][neighbor_y-1])
        if neighbor_x > 0 and neighbor_y <rows -1:
            self.neighbors.append(grid[neighbor_x-1][neighbor_y+1])
        if neighbor_x < columns -1 and neighbor_y < rows -1:
            self.neighbors.append(grid[neighbor_x+1][neighbor_y+1]) """


class AStarMovement:
    def __init__(self):
        self.direction_list = []
    @staticmethod
    def clean_open_set(open_set, current_node):

        for i in range(len(open_set)):
            if open_set[i] == current_node:
                open_set.pop(i)
                break

        return open_set

    @staticmethod
    def h_score(current_node, end):

        distance = abs(current_node.x - end.x) + abs(current_node.y - end.y)

        return distance

    @staticmethod
    def create_grid(cols, rows):

        grid = []
        for _ in range(cols):
            grid.append([])
            for _ in range(rows):
                grid[-1].append(0)

        return grid

    @staticmethod
    def fill_grids(grid, cols, rows, obstacle_ratio=False, obstacle_list=False):

        for i in range(cols):
            for j in range(rows):
                grid[i][j] = Node(i, j)
                if obstacle_ratio == False:
                    pass
                else:
                    n = randint(0, 100)
                    if n < obstacle_ratio: grid[i][j].obstacle = True
        if obstacle_list == False:
            pass
        else:
            for i in range(len(obstacle_list)):
                grid[obstacle_list[i][0]][obstacle_list[i][1]].obstacle = True

        return grid

    @staticmethod
    def get_neighbors(grid, cols, rows):
        for i in range(cols):
            for j in range(rows):
                grid[i][j].add_neighbors(grid, cols, rows)
        return grid

    @staticmethod
    def start_path(open_set, closed_set, current_node, end):

        best_way = 0
        for i in range(len(open_set)):
            if open_set[i].f < open_set[best_way].f:
                best_way = i

        current_node = open_set[best_way]
        final_path = []
        if current_node == end:
            temp = current_node
            while temp.previous:
                final_path.append(temp.previous)
                temp = temp.previous

        open_set = AStarMovement.clean_open_set(open_set, current_node)
        closed_set.append(current_node)
        neighbors = current_node.neighbors
        for neighbor in neighbors:
            if (neighbor in closed_set) or (neighbor.obstacle == True):
                continue
            else:
                temp_g = current_node.g + 1
                control_flag = 0
                for k in range(len(open_set)):
                    if neighbor.x == open_set[k].x and neighbor.y == open_set[k].y:
                        if temp_g < open_set[k].g:
                            open_set[k].g = temp_g
                            open_set[k].h = AStarMovement.h_score(open_set[k], end)
                            open_set[k].f = open_set[k].g + open_set[k].h
                            open_set[k].previous = current_node
                        else:
                            pass
                        control_flag = 1

                if control_flag == 1:
                    pass
                else:
                    neighbor.g = temp_g
                    neighbor.h = AStarMovement.h_score(neighbor, end)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.previous = current_node
                    open_set.append(neighbor)

        return open_set, closed_set, current_node, final_path

    def astar(self, rows, cols, start, end, obstacle_ratio=False, obstacle_list=False):
        grid = AStarMovement.create_grid(cols, rows)
        grid = AStarMovement.fill_grids(grid, cols, rows, obstacle_ratio=obstacle_ratio,
                                obstacle_list=obstacle_list)
        grid = AStarMovement.get_neighbors(grid, cols, rows)
        open_set = []
        closed_set = []
        current_node = None
        final_path = []
        open_set.append(grid[start[0]][start[1]])
        end = grid[end[0]][end[1]]
        while len(open_set) > 0:
            open_set, closed_set, current_node, final_path = AStarMovement.start_path(open_set, closed_set, current_node,
                                                                              end)
            if len(final_path) > 0:
                break

        path_list = []
        for i in range(len(final_path)):
            next_step = (final_path[i].x, final_path[i].y)
            path_list.append(next_step)
        path_list.insert(0, (end.x, end.y))
        path_list.reverse()

        return path_list

    def get_maze(self, snake_body):
        maze = [[0] * param.WIDTH for i in range(param.HEIGHT)]
        for el in snake_body:
            maze[el[1]][el[0]] = 1
        return maze

    def get_path(self, snake, apple_location):
        maze = self.get_maze(snake.body)
        path = self.astar(param.HEIGHT, param.WIDTH, snake.head, apple_location, obstacle_ratio=False, obstacle_list=snake.body)
        return path

    def path_to_direction_list(self, path):
        direction_list = []
        for k in range(len(path) - 1):
            direction = tuple(map(lambda i, j: i - j, path[k + 1], path[k]))
            direction_list.append(direction)
        return direction_list

    def get_direction(self, key_list, snake, apple):
        if len(self.direction_list) == 0:
            path = self.get_path(snake, apple.location)
            self.direction_list = self.path_to_direction_list(path)
        try:
            direction = self.direction_list[0]
            self.direction_list.pop(0)
            return direction
        except IndexError:
            return None
