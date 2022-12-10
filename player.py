from pygame.locals import *
from glm import vec3, vec2
import pygame
import glm

from camera import Camera

SPEED = 0.004
GRAVITY = 0.0005
JUMP_VEL = 0.01

class Player:
    def __init__(self, manager):
        self.manager = manager
        self.aspect_ratio = manager.WIDTH / manager.HEIGHT
        self.pos = vec3(0, 2, 0)
        self.vel = vec3(0, 0, 0)
        self.size = vec3(0.6, 1.8, 1.8)
        self.camera = Camera(manager, self)
        self.on_ground = False

    def update(self):
        self.camera.update()

        self.vel.y -= GRAVITY
        self.pos += self.vel * self.manager.dt

        keys = pygame.key.get_pressed()
        if keys[K_a]:
            self.pos -= self.camera.right * SPEED * self.manager.dt
        if keys[K_d]:
            self.pos += self.camera.right * SPEED * self.manager.dt
        if keys[K_s]:
            self.pos -= glm.normalize(vec3(self.camera.forward.x, 0, self.camera.forward.z)) * SPEED * self.manager.dt
        if keys[K_w]:
            self.pos += glm.normalize(vec3(self.camera.forward.x, 0, self.camera.forward.z)) * SPEED * self.manager.dt
        if keys[K_SPACE] and self.on_ground:
            self.vel.y = JUMP_VEL

        self.on_ground = False
        if self.pos.y < 0 + self.size.y:
            self.on_ground = True
            self.pos.y = 0 + self.size.y