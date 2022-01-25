import pygame
import parameters
import numpy as np

class Game:
    def __init__(self, snake, apple, display, movement=0):
        self.snake = snake()
        self.apple = apple()
        self.direction = (1, 0)
        self.snake_clone = snake
        self.apple_clone = apple
        self.display = display()
        self.movement = movement
        self.clock = pygame.time.Clock()
        self.is_game_over = False
        self.score = 0
        self.count = 0
        self.frame_iteration = 0
        self.right_key, self.left_key, self.down_key, self.up_key = False, False, False, False
        self.iteration = 0
        self.plot_iteration = []
        self.plot_score = []
        self.plot_mean_score = []


    def run(self):
        while not self.is_game_over:
            if self.count == 0:
                self.display.update(self.snake, self.apple, self.score)
                self.clock.tick(parameters.FPS)
                self.count += 1
            else:
                self.play_step()

    def reset(self):
        self.plot_score.append(self.score)
        self.plot_iteration.append(str(self.iteration))
        self.plot_mean_score.append(sum(self.plot_score) / len(self.plot_iteration))
        self.iteration += 1
        self.frame_iteration = 0
        self.count = 0
        self.reset_keys()
        self.right_key = True
        self.direction = (1, 0)
        self.score = 0
        self.snake = self.snake_clone()
        self.apple = self.apple_clone()
        self.display.score_plot(self.plot_score, self.plot_iteration, self.plot_mean_score)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.right_key = True
                    self.left_key, self.down_key, self.up_key = False, False, False
                elif event.key == pygame.K_LEFT:
                    self.left_key = True
                    self.right_key, self.down_key, self.up_key = False, False, False
                elif event.key == pygame.K_DOWN:
                    self.down_key = True
                    self.left_key, self.right_key, self.up_key = False, False, False
                elif event.key == pygame.K_UP:
                    self.up_key = True
                    self.left_key, self.down_key, self.right_key = False, False, False
                elif event.key == pygame.K_ESCAPE:
                    print(self.score)
                    pygame.quit()
                    quit()
            if event.type == pygame.QUIT:
                print(self.score)
                pygame.quit()
                quit()

    def reset_keys(self):
        self.right_key, self.left_key, self.down_key, self.up_key = False, False, False, False

    def check_if_game_is_over(self):
        if self.snake.is_collision() or self.snake.is_out_of_boundary():
            return True
        return False

    def play_step(self, direction=None):
        self.frame_iteration += 1
        self.check_events()
        key_arrows = [self.right_key, self.left_key, self.up_key, self.down_key]
        if self.movement != 0:
            direction = self.movement.get_direction(key_arrows, self.snake, self.apple)  # get direction as a tuple

        self.direction = direction

        if direction is not None:
            self.snake.move(direction, self.apple.location)  # move the snake given the direction
            reward = 0
            if self.check_if_game_is_over() is True or self.frame_iteration > 100*len(self.snake.body):
                self.is_game_over = True

            if not self.is_game_over:
                # check if apple was eaten and place a new one if it was
                was_apple_eaten = self.snake.was_apple_eaten(self.apple.location)
                if was_apple_eaten:
                    self.score += 1
                    reward = 10
                    snake_area = [self.snake.head] + self.snake.body
                    self.apple.place_food(snake_area)

                # display new location of the snake and apple, change score
                self.display.update(self.snake, self.apple, self.score)

                # makes the game run max param.FPS frames per sec
                self.clock.tick(parameters.FPS)

            elif self.is_game_over:
                self.is_game_over = False
                if self.movement != 0:
                    self.reset()
                reward = -10
                return reward, True, self.score

            return reward, self.is_game_over, self.score

        else:
            print("path not found")
            self.is_game_over = True
            if self.is_game_over:
                self.reset()
                self.is_game_over = False

    def get_state(self):

        point_l = (self.snake.head[0] - 1, self.snake.head[1])
        point_r = (self.snake.head[0] + 1, self.snake.head[1])
        point_u = (self.snake.head[0], self.snake.head[1] - 1)
        point_d = (self.snake.head[0], self.snake.head[1] + 1)

        dir_l = self.direction == (-1, 0)
        dir_r = self.direction == (1, 0)
        dir_u = self.direction == (0, -1)
        dir_d = self.direction == (0, 1)

        state = [
            # Danger up
            self.snake.is_collision(point_u) or
            self.snake.is_out_of_boundary(point_u),

            # Danger down
            self.snake.is_collision(point_d) or
            self.snake.is_out_of_boundary(point_d),

            # Danger left
            self.snake.is_collision(point_l) or
            self.snake.is_out_of_boundary(point_l),

            # Danger right
            self.snake.is_collision(point_r) or
            self.snake.is_out_of_boundary(point_r),

            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Food location
            self.apple.location[0] < self.snake.head[0],  # food left
            self.apple.location[0] > self.snake.head[0],  # food right
            self.apple.location[1] < self.snake.head[1],  # food up
            self.apple.location[1] > self.snake.head[1]  # food down
        ]
        return np.array(state, dtype=int)