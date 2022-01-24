import pygame
import matplotlib.pyplot as plt
import param


class Display:
    def __init__(self):
        pygame.init()
        plt.ion()
        self.font = pygame.font.SysFont("comicsans", 40)
        self.display = pygame.display.set_mode((param.WIDTH * param.BLOCK_SIZE, param.HEIGHT * param.BLOCK_SIZE))
        pygame.display.set_caption("Snake")

    def reset(self):
        self.font = pygame.font.SysFont("comicsans", 40)
        self.display = pygame.display.set_mode((param.WIDTH * param.BLOCK_SIZE, param.HEIGHT * param.BLOCK_SIZE))
        pygame.display.set_caption("Snake")

    def update(self, snake, apple, score):
        self.display.fill(param.BLACK)
        txt = self.font.render("Score:" + str(score), True, param.WHITE)
        self.display.blit(txt, [0, 0])

        for el in snake.get_mask():
            pygame.draw.rect(self.display, el[2], pygame.Rect(el[0] * param.BLOCK_SIZE, el[1] * param.BLOCK_SIZE, param.BLOCK_SIZE, param.BLOCK_SIZE))

        for el in apple.get_mask():
            pygame.draw.rect(self.display, el[2], pygame.Rect(el[0] * param.BLOCK_SIZE, el[1] * param.BLOCK_SIZE, param.BLOCK_SIZE, param.BLOCK_SIZE))

        pygame.display.flip()

    def score_plot(self, score, iteration, mean):
        plt.clf()
        if len(score) == 1:
            plt.scatter(iteration, score, label="score")
            plt.scatter(iteration, mean, label="mean score")
        else:
            plt.plot(iteration, score, label="score")
            plt.plot(iteration, mean, label="mean score")
        plt.ylabel("Score")
        plt.xlabel("Iteration")
        plt.legend()
        plt.show()
        plt.pause(.1)
