import pyglet
from pyglet.gl import *

window = pyglet.window.Window(width=720, height=480)
window.projection = pyglet.window.Projection3D()
batch = pyglet.graphics.Batch()


@window.event
def on_draw():
    window.clear()
    batch.draw()


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    glRotatef(1, dx, dy, 0)


def rotate(dt):
    glRotatef(0.5, dt, dt, dt)


if __name__ == "__main__":
    glEnable(GL_MULTISAMPLE_ARB)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    model = pyglet.model.load("/data/waffle1/crawl/objaverse/hf-objaverse-v1/glbs/000-047/54001647c1084605aad7525370d93bb8.glb", batch=batch)
    glTranslatef(0, 0, -3)
    pyglet.clock.schedule_interval(rotate, 1/60)
    pyglet.app.run()