import pygame
import sys
from settings import *
from level import Level


class Game:
    # Constructor.
    def __init__(self):

        # General Setup.
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixel RPG 🤌")
        self.clock = pygame.time.Clock()

        self.level = Level()

    # Method to run the game.
    def run(self):
        # Event loop.
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Create a screen that is updated and clock moves according to set fps.
            self.screen.fill("black")
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
