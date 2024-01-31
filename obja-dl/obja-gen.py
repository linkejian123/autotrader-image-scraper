import os
import pygame
from pygame.locals import *
from pyglet.gl import *
import pyglet
import pyassimp

# Function to get all GLB paths in a folder
def get_glb_paths(folder):
    glb_paths = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".glb"):
                glb_paths.append(os.path.join(root, file))
    return glb_paths

def render_model(glb_path):
    glEnable(GL_DEPTH_TEST)
    glClearColor(1, 1, 1, 1)

    # Load the GLB model using PyAssimp
    scene = pyassimp.load(glb_path)

    vertices = scene.meshes[0].vertices
    normals = scene.meshes[0].normals

    # Use Pyglet Batch for rendering
    batch = pyglet.graphics.Batch()
    batch.add(len(vertices) // 3, GL_TRIANGLES, None,
              ('v3f/static', vertices),
              ('n3f/static', normals))

    pyassimp.release(scene)  # Release the loaded scene data

    @window.event
    def on_draw():
        window.clear()
        glLoadIdentity()
        gluPerspective(60, window.width / float(window.height), 0.1, 100.0)
        glTranslatef(0, 0, -3)
        glRotatef(0.5, 1, 1, 0)
        batch.draw()

    # Return the batch for additional operations if needed
    return batch

# Function to display the snapshot using Pygame
def display_snapshot(image_path):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('GLB Viewer')
    snapshot = pygame.image.load(image_path)
    screen.blit(snapshot, (0, 0))
    pygame.display.flip()

# Function to display the snapshot using Pygame
def display_snapshot(image_path):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('GLB Viewer')
    snapshot = pygame.image.load(image_path)
    screen.blit(snapshot, (0, 0))
    pygame.display.flip()

# Main script
glb_src_folder = r'/data/waffle1/crawl/objaverse/hf-objaverse-v1/glbs/'
output_folder = r'/data/waffle1/crawl/objaverse/hf-objaverse-v1/images/'

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Get a list of GLB files
glb_paths = get_glb_paths(glb_src_folder)

# Initialize marked list with zeros
marked_list = [0] * len(glb_paths)

# Zip glb_paths and marked_list
zipped_data = list(zip(glb_paths, marked_list))
print(zipped_data)


# Initialize Pygame
pygame.init()

# Initialize Pyglet
pyglet.options['shadow_window'] = False

# Function to create a Pyglet window and render GLB model
def render_pyglet_window(glb_path):
    window = pyglet.window.Window(width=800, height=600, resizable=True)

    @window.event
    def on_draw():
        window.clear()
        glLoadIdentity()
        gluPerspective(60, window.width / float(window.height), 0.1, 100.0)
        glTranslatef(0, 0, -3)
        glRotatef(0.5, 1, 1, 0)
        render_model(glb_path)

    pyglet.app.run()


# Iterate through each GLB file
index = 0
while index < len(zipped_data):
    glb_path, mark = zipped_data[index]
    render_model(glb_path)
    
    # Save snapshot
    snapshot_path = os.path.join(output_folder, f'image_{index}.png')
    display_snapshot(snapshot_path)

    # Wait for user input
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_n:
                    index = (index + 1) % len(zipped_data)
                    waiting_for_input = False
                elif event.key == K_m:
                    marked_list[index] = 1
                    index = (index + 1) % len(zipped_data)
                    waiting_for_input = False

# Display the final marked list
print("Final Marked Models:")
for model_path, mark in zipped_data:
    print(f'Model: {model_path}, Mark: {mark}')