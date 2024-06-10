import bpy
import os
import math
from mathutils import Vector 

path_to_glb_folder = "/data/waffle1/crawl/objaverse/hf-objaverse-v1/glbs/000-000/f8024595e11c48119877c9c7cc554abc.glb"
path_to_jpeg_folder = "/data/waffle1/crawl/objaverse/hf-objaverse-v1/images/"
num_photos = 20  # Number of photos to capture (360 degrees / 60 degrees interval)

def delete_all_objects():
    """
    Deletes all objects in the current scene
    """
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

delete_all_objects()

# List all glb files in the specified folder
glb_file_list = [f for f in os.listdir(path_to_glb_folder) if f.lower().endswith('.glb')]

for glb_file in glb_file_list:
    # Import glb file
    bpy.ops.import_scene.gltf(filepath=os.path.join(path_to_glb_folder, glb_file))

    # Set up camera and light
    bpy.ops.object.camera_add(location=(0, 0, 7), rotation=(math.radians(90), 0, math.radians(45)))
    bpy.ops.object.light_add(type='POINT', location=(0, 0, 10))
    
    # Set render settings
    bpy.context.scene.render.image_settings.file_format = "JPEG"

    # Animate the camera in a circular motion
    for frame in range(num_photos):
        angle = frame * (2 * math.pi) / num_photos
        bpy.context.object.location = (7 * math.cos(angle), 7 * math.sin(angle), 7)
        bpy.context.scene.frame_set(frame + 1)
        
        # Render image for each frame
        bpy.context.scene.render.filepath = os.path.join(path_to_jpeg_folder, f"{glb_file.replace('.glb', '_')}_{frame + 1}.jpg")
        bpy.ops.render.render(write_still=True)

    # Reset frame to 1 for the next glb file
    bpy.context.scene.frame_set(1)

    delete_all_objects()