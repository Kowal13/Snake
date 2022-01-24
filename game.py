import pygame
import param


class Game:
    def __init__(self, snake, apple, display, movement):
        self.snake = snake
        self.apple = apple
        self.display = display
        self.movement = movement
        self.clock = pygame.time.Clock()
        self.is_game_over = False
        self.score = 0
        self.game_iteration = 1
        self.plot_score = []
        self.plot_iteration = []
        self.plot_mean_score = []
        self.esc_key, self.right_key, self.left_key, self.down_key, self.up_key = False, False, False, False, False

    def run(self, run_forever=True):
        self.game_iteration += 1
        while not self.is_game_over:
            self.check_events()
            self.play_step()
            if self.is_game_over:
                if self.esc_key:
                    pygame.quit()
                    quit()
                if run_forever:
                    self.reset()
                    self.is_game_over = False
        print(self.score)
        pygame.quit()

    def reset(self):
        self.game_iteration += 1
        self.plot_score.append(self.score)
        self.plot_iteration.append(str(self.game_iteration))
        self.display.reset()
        self.snake.__init__()
        self.apple.__init__()
        self.plot_mean_score.append(sum(self.plot_score) / len(self.plot_iteration))
        self.display.score_plot(self.plot_score, self.plot_iteration, self.plot_mean_score)
        self.score = 0
        self.reset_keys()
        self.movement.reset()

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
                    self.esc_key = True
            if event.type == pygame.QUIT:
                self.esc_key = True

    def reset_keys(self):
        self.right_key, self.left_key, self.down_key, self.up_key, self.esc_key = False, False, False, False, False

    def check_if_game_is_over(self):
        if self.snake.is_collision() or self.snake.is_out_of_boundary() or self.esc_key:
            return True
        return False

    def play_step(self):
        # makes the game run max param.FPS frames per sec
        self.clock.tick(param.FPS)

        key_arrows = [self.right_key, self.left_key, self.up_key, self.down_key]
        direction = self.movement.get_direction(key_arrows, self.snake, self.apple)  # get direction as a tuple

        if direction is not None:
            self.snake.move(direction, self.apple.location)  # move the snake given the direction

            self.is_game_over = self.check_if_game_is_over()

            if not self.is_game_over:
                # check if apple was eaten and place a new one if it was
                was_apple_eaten = self.snake.was_apple_eaten(self.apple.location)
                if was_apple_eaten:
                    self.score += 1
                    snake_area = [self.snake.head] + self.snake.body
                    self.apple.place_food(snake_area)

                # display new location of the snake and apple, change score
                self.display.update(self.snake, self.apple, self.score)

        else:
            print("no path found")
            self.is_game_over = True
