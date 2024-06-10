import bpy
import os
import math

path_to_glb_folder = "/data/waffle1/crawl/objaverse/hf-objaverse-v1/glbs/"
path_to_jpeg_folder = "/data/waffle1/crawl/objaverse/hf-objaverse-v1/images/"
num_photos = 6  # Number of photos to capture (360 degrees / 60 degrees interval)

def deleteAllObjects():
    """
    Deletes all objects in the current scene
    """
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

def get_bounding_box_center(obj):
    """
    Get the center of the bounding box of the object
    """
    # Get the bounding box coordinates in object space
    bbox_coords = [Vector(b) for b in obj.bound_box]

    # Calculate the center of the bounding box in object space
    bbox_center_obj_space = sum(bbox_coords, Vector()) / 8
    
    # Convert the bounding box center to world space
    bbox_center_world_space = obj.matrix_world @ bbox_center_obj_space
    
    return bbox_center_world_space

deleteAllObjects()

glb_dirList = [f for f in os.listdir(path_to_glb_folder) if f.lower().endswith('.glb')]

for i in glb_dirList:
    print(i)
    bpy.ops.import_scene.gltf(filepath=os.path.join(path_to_glb_folder, i))  # Import .glb file to scene

    # Add light (Point light with increased energy)
    bpy.ops.object.light_add(type='POINT', location=(0, 0, 10))
    light_object = bpy.context.object
    light_object.data.energy = 1000  # Adjust the energy value

    # Get the imported object
    imported_obj = bpy.context.view_layer.objects.active

    # Calculate the bounding box center of the imported object
    bbox_center = get_bounding_box_center(imported_obj)

    # Create a new material for the bounding box
    material = bpy.data.materials.new(name="BoundingBoxMaterial")
    material.diffuse_color = (1, 0, 0, 1)  # Set color to red (RGB values, alpha)

    # Create a new mesh object representing the bounding box
    bpy.ops.mesh.primitive_cube_add(size=2, location=bbox_center)
    bounding_box = bpy.context.active_object
    bounding_box.name = "BoundingBox"
    bounding_box.data.materials.append(material)  # Assign the material to the bounding box

    # Set up camera with wide angle (focal length 20mm) revolving around the bounding box center
    bpy.ops.object.camera_add(location=(bbox_center.x + 7, bbox_center.y + 7, bbox_center.z + 7),
                              rotation=(math.radians(45), 0, math.radians(45)))
    scene = bpy.context.scene
    camera = bpy.context.object
    camera.data.lens = 20  # Set focal length to 20mm
    scene.camera = camera

    # Set render settings
    bpy.context.scene.render.filepath = os.path.join(path_to_jpeg_folder, i.replace('.glb', '_'))  # Set save path for images
    bpy.context.scene.render.image_settings.file_format = "JPEG"  # Set image file format

    # Adjust exposure and contrast in camera settings
    bpy.context.scene.view_settings.view_transform = 'Filmic'
    bpy.context.scene.view_settings.look = 'High Contrast'
    
    # Set the number of samples for Cycles render engine
    bpy.context.scene.cycles.samples = 500  # Adjust the number of render samples for Cycles
    
    # Set the number of samples for Eevee render engine
    # bpy.context.scene.eevee.taa_render_samples = 16  # Adjust the number of render samples for Eevee

    # Animate the camera in a circular motion
    for frame in range(num_photos):
        angle = frame * (2 * math.pi) / num_photos
        camera.location = (5 * math.cos(angle) + bbox_center.x + 7,
                           5 * math.sin(angle) + bbox_center.y + 7,
                           5 + bbox_center.z)
        camera.rotation_euler = (math.radians(45), 0, math.radians(45) - angle)
        bpy.context.scene.frame_set(frame + 1)
        
        # Construct the file name using the glb name and photo number
        file_name = "{}_{}.jpg".format(i.replace('.glb', ''), frame + 1)
        bpy.context.scene.render.filepath = os.path.join(path_to_jpeg_folder, file_name)

        bpy.ops.render.render(write_still=True)  # Render image for each frame

    deleteAllObjects()