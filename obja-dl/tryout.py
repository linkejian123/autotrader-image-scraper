import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pyassimp

def render_scene(scene):
    for mesh in scene.meshes:
        vertices = mesh.vertices
        normals = mesh.normals

        glBegin(GL_TRIANGLES)
        for i in range(0, len(vertices), 3):
            glVertex3fv(vertices[i:i+3])
            glNormal3fv(normals[i:i+3])
        glEnd()

def display_glb_snapshot(glb_file):
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Load the GLB model using PyAssimp
        scene = pyassimp.load(glb_file)

        if scene.meshes:
            render_scene(scene)

        pyassimp.release(scene)  # Release the loaded scene data

        pygame.display.flip()
        pygame.time.wait(10)




# Example usage:
display_glb_snapshot("/data/waffle1/crawl/objaverse/hf-objaverse-v1/glbs/000-113/8a8f31ffd28748f9bde769ac82cd882c.glb")