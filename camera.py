from pygame.locals import *
from glm import vec3, vec2
import pygame
import glm

FOV = 75
NEAR = 0.01
FAR = 100
SPEED = 0.004
SENSITIVITY = 0.16

class Camera:
    def __init__(self, manager):
        self.manager = manager
        self.aspect_ratio = manager.WIDTH / manager.HEIGHT
        self.pos = vec3(0, 2, 0)
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
            self.yaw += rel_x * SENSITIVITY
            self.pitch -= rel_y * SENSITIVITY
            self.pitch = max(-89, min(89, self.pitch))
            
            yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)
            self.forward.x = glm.cos(yaw) * glm.cos(pitch)
            self.forward.y = glm.sin(pitch)
            self.forward.z = glm.sin(yaw) * glm.cos(pitch)
            self.forward = glm.normalize(self.forward)
            self.right = glm.normalize(glm.cross(self.forward, vec3(0, 1, 0)))

        keys = pygame.key.get_pressed()
        if keys[K_a]:
            self.pos -= self.right * SPEED * self.manager.dt
        if keys[K_d]:
            self.pos += self.right * SPEED * self.manager.dt
        if keys[K_s]:
            self.pos -= glm.normalize(vec3(self.forward.x, 0, self.forward.z)) * SPEED * self.manager.dt
        if keys[K_w]:
            self.pos += glm.normalize(vec3(self.forward.x, 0, self.forward.z)) * SPEED * self.manager.dt
        if keys[K_LSHIFT]:
            self.pos -= self.up * SPEED * self.manager.dt
        if keys[K_SPACE]:
            self.pos += self.up * SPEED * self.manager.dt

        self.m_view = self.get_view_matrix()

    def get_view_matrix(self):
        return glm.lookAt(self.pos, self.pos + self.forward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)