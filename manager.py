from pygame.locals import *
import moderngl as gl
import pygame
import sys

from player import Player
from model import *

class Manager:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1400, 800
        pygame.display.gl_set_attribute(GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(GL_CONTEXT_PROFILE_MASK, GL_CONTEXT_PROFILE_CORE)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), OPENGL | DOUBLEBUF)
        pygame.mouse.set_visible(False)
        self.context = gl.create_context()
        self.context.enable(gl.DEPTH_TEST | gl.CULL_FACE)
        self.clock = pygame.time.Clock()
        self.time = 0
        self.dt = 0
        self.player = Player(self)
        self.camera = self.player.camera
        self.blocks = []
        for x in range(-10, 11):
            for z in range(-10, 11):
                Block(self, (x, 0, z))
        self.paused = False
        self.first_pause = True

    def update(self):
        self.dt = self.clock.tick(60)
        self.time = pygame.time.get_ticks()
        pygame.display.set_caption(f"{round(self.clock.get_fps())}")

        self.first_pause = not self.paused

        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.paused = not self.paused
                    pygame.mouse.set_visible(self.paused)

        self.player.update()
        for block in self.blocks:
            block.update()

        if not self.paused:
            pygame.mouse.set_pos((self.WIDTH // 2, self.HEIGHT // 2))

    def draw(self):
        self.context.clear(color=(0.08, 0.16, 0.18))
        for block in self.blocks:
            block.draw()
        pygame.display.flip()

    def run(self):
        while True:
            self.update()
            self.draw()

    def quit(self):
        for block in self.blocks:
            block.destroy()
        pygame.quit()
        sys.exit()