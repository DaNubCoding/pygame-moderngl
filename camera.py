from pygame.locals import *
from glm import vec3, vec2
import pygame
import glm

FOV = 75
NEAR = 0.01
FAR = 100
SPEED = 0.004
SENSITIVITY = 0.02

class Camera:
    def __init__(self, manager, player):
        self.manager = manager
        self.player = player
        self.aspect_ratio = manager.WIDTH / manager.HEIGHT
        self.pos = player.pos
        self.up = vec3(0, 1, 0)
        self.right = vec3(1, 0, 0)
        self.forward = vec3(0, 0, -1)
        self.yaw = -90
        self.pitch = 0
        self.m_view = self.get_view_matrix()
        self.m_proj = self.get_projection_matrix()

    def update(self):
        if not self.manager.paused and self.manager.first_pause:
            rel_x, rel_y = vec2(pygame.mouse.get_pos()) - vec2(self.manager.WIDTH // 2, self.manager.HEIGHT // 2)
            self.yaw += rel_x * SENSITIVITY * self.manager.dt
            self.pitch -= rel_y * SENSITIVITY * self.manager.dt
            self.pitch = max(-89, min(89, self.pitch))
            
            yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)
            self.forward.x = glm.cos(yaw) * glm.cos(pitch)
            self.forward.y = glm.sin(pitch)
            self.forward.z = glm.sin(yaw) * glm.cos(pitch)
            self.forward = glm.normalize(self.forward)
            self.right = glm.normalize(glm.cross(self.forward, vec3(0, 1, 0)))

        self.pos = self.player.pos

        self.m_view = self.get_view_matrix()

    def get_view_matrix(self):
        return glm.lookAt(self.pos, self.pos + self.forward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)