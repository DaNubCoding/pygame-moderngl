import numpy as np
import pygame
import glm

class Block:
    def __init__(self, manager, pos):
        self.manager = manager
        self.manager.blocks.append(self)
        self.context = self.manager.context
        self.pos = pos
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program("default")
        self.vao = self.get_vao()
        self.m_model = self.get_model_matrix()
        self.texture = self.get_texture("textures/dirt.png")
        self.texture.use()
        self.shader_program["u_texture"] = 0
        self.shader_program["m_proj"].write(self.manager.camera.m_proj)
        self.shader_program["m_view"].write(self.manager.camera.m_view)
        self.shader_program["m_model"].write(self.m_model)

    def update(self):
        self.shader_program["m_proj"].write(self.manager.camera.m_proj)
        self.shader_program["m_view"].write(self.manager.camera.m_view)
        self.shader_program["m_model"].write(self.m_model)

    def draw(self):
        self.vao.render()

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_texture(self, path):
        texture = pygame.image.load(path).convert()
        texture = pygame.transform.scale(texture, (1024, 1024))
        texture = pygame.transform.flip(texture, False, True)
        texture = self.context.texture(texture.get_size(), 3, pygame.image.tostring(texture, "RGB"))
        return texture

    def get_model_matrix(self):
        m_model = glm.mat4()
        return m_model

    def get_vao(self):
        vao = self.context.vertex_array(self.shader_program, [(self.vbo, "2f 3f", "in_texcoord", "in_position")])
        return vao

    def get_vertext_data(self):
        vertices = np.asarray([(-1, -1, 1), (0, -1, 1), (0, 0, 1), (-1, 0, 1),
                    (-1, 0, 0), (-1, -1, 0), (0, -1, 0), (0, 0, 0)])
        vertices = np.add(vertices, [self.pos] * 8)
        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        vertex_data = self.get_data(vertices, indices)

        tex_coord = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [(0, 2, 3), (0, 1, 2),
                             (0, 2, 3), (0, 1, 2),
                             (0, 1, 2), (2, 3, 0),
                             (2, 3, 0), (2, 0, 1),
                             (0, 2, 3), (0, 1, 2),
                             (3, 1, 2), (3, 0, 1)]
        tex_coord_data = self.get_data(tex_coord, tex_coord_indices)
        vertex_data = np.hstack([tex_coord_data, vertex_data])

        return vertex_data

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype="f4")

    def get_vbo(self):
        vertext_data = self.get_vertext_data()
        vbo = self.context.buffer(vertext_data)
        return vbo

    def get_shader_program(self, shader_name):
        with open(f"shaders/{shader_name}.vert") as file:
            vertex_shader = file.read()
        with open(f"shaders/{shader_name}.frag") as file:
            fragment_shader = file.read()

        program = self.context.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program