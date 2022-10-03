import pygame
from utils import *
from editor import Editor

class Level:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width,screen_height))
        self.display_surface = pygame.display.get_surface()
        self.editor = Editor()

    def run(self):
        self.editor.run()


if __name__ == "__main__":
    Level().run()