import pygame
import parameters
import matplotlib.pyplot as plt

plt.ion()


class Display:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont("comicsans", 40)
        self.display = pygame.display.set_mode((parameters.WIDTH * parameters.BLOCK_SIZE, parameters.HEIGHT * parameters.BLOCK_SIZE))
        pygame.display.set_caption("Snake")

    def update(self, snake, apple, score):
        self.display.fill(parameters.BLACK)
        txt = self.font.render("Score:" + str(score), True, parameters.WHITE)
        self.display.blit(txt, [0, 0])

        for el in snake.get_mask():
            pygame.draw.rect(self.display, el[2], pygame.Rect(el[0] * parameters.BLOCK_SIZE, el[1] * parameters.BLOCK_SIZE, parameters.BLOCK_SIZE, parameters.BLOCK_SIZE))

        for el in apple.get_mask():
            pygame.draw.rect(self.display, el[2], pygame.Rect(el[0] * parameters.BLOCK_SIZE, el[1] * parameters.BLOCK_SIZE, parameters.BLOCK_SIZE, parameters.BLOCK_SIZE))

        pygame.display.flip()

    def score_plot(self, score, iteration, mean):
        plt.clf()
        plt.plot(score, label="score")
        plt.plot(mean, label="mean score")
        plt.ylabel("Score")
        plt.xlabel("Iteration")
        plt.legend()
        plt.show()
        plt.pause(.1)