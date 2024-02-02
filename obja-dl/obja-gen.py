import bpy
import os
import math
from mathutils import Vector 

path_to_glb_folder = "/data/waffle1/crawl/objaverse/hf-objaverse-v1/glbs/000-000/"
path_to_jpeg_folder = "/data/waffle1/crawl/objaverse/hf-objaverse-v1/images/"
num_photos = 20  # Number of photos to capture (360 degrees / 60 degrees interval)

def deleteAllObjects():
    """
    Deletes all objects in the current scene
    """
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

deleteAllObjects()

glb_dirList = [f for f in os.listdir(path_to_glb_folder) if f.lower().endswith('.glb')]

for i in glb_dirList:
    print(i)
    bpy.ops.import_scene.gltf(filepath=os.path.join(path_to_glb_folder, i))  # Import .glb file to scene

    # Get the imported object
    imported_obj = bpy.context.view_layer.objects.active

    # Check if the imported object is a mesh
    if imported_obj and imported_obj.type == 'MESH':
        # Get the object's location
        obj_location = imported_obj.location

        # Duplicate the object and link the duplicate to the scene
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = imported_obj
        bpy.ops.object.duplicate(linked=False)
        bounding_box = bpy.context.view_layer.objects.active
        bounding_box.name = "BoundingBox"

        # Set up camera with wide angle (focal length 20mm) revolving around the bounding box center
        bpy.ops.object.camera_add(location=(obj_location.x, obj_location.y, obj_location.z + 7),
                                  rotation=(math.radians(90), 0, math.radians(45)))
        scene = bpy.context.scene
        camera = bpy.context.object
        camera.data.lens = 20  # Set focal length to 20mm
        scene.camera = camera

        # Add light (Point light with increased energy)
        bpy.ops.object.light_add(type='POINT', location=(0, 0, 10))
        light_object = bpy.context.object
        light_object.data.energy = 1000  # Adjust the energy value

        # Set render settings
        bpy.context.scene.render.filepath = os.path.join(path_to_jpeg_folder, i.replace('.glb', '_'))  # Set save path for images
        bpy.context.scene.render.image_settings.file_format = "JPEG"  # Set image file format

        # Animate the camera in a circular motion
        for frame in range(num_photos):
            angle = frame * (2 * math.pi) / num_photos
            camera.location = (7 * math.cos(angle) + obj_location.x,
                               7 * math.sin(angle) + obj_location.y,
                               obj_location.z + 7)

            # Set the camera rotation to always point towards the bounding box center
            camera.rotation_euler = (math.radians(90), 0, math.atan2(obj_location.y - camera.location.y,
                                                                     obj_location.x - camera.location.x) + math.radians(45))

            bpy.context.scene.frame_set(frame + 1)

            # Render image for each frame
            bpy.ops.render.render(write_still=True)

        deleteAllObjects()