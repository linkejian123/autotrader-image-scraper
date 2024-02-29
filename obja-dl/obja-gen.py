## generate picture from blender using glb file

import bpy
import os
import math
from mathutils import Vector 
import numpy as np

## This made from blender build in 
path_to_glb_folder = "/data/waffle1/crawl/objaverse/bikes/bicycle.glb" #4abc good
path_to_jpeg_folder = "/data/waffle1/crawl/objaverse/bikes/images/"
num_photos = 20  # Number of photos to capture (360 degrees / 60 degrees interval)


def purge_orphans():
    if bpy.app.version >= (3, 0, 0):
        bpy.ops.outliner.orphans_purge(
            do_local_ids=True, do_linked_ids=True, do_recursive=True
        )
    else:
        # call purge_orphans() recursively until there are no more orphan data blocks to purge
        result = bpy.ops.outliner.orphans_purge()
        if result.pop() != "CANCELLED":
            purge_orphans()


def clean_scene():
    """
    Removing all of the objects, collection, materials, particles,
    textures, images, curves, meshes, actions, nodes, and worlds from the scene
    """
    if bpy.context.active_object and bpy.context.active_object.mode == "EDIT":
        bpy.ops.object.editmode_toggle()

    for obj in bpy.data.objects:
        obj.hide_set(False)
        obj.hide_select = False
        obj.hide_viewport = False

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    collection_names = [col.name for col in bpy.data.collections]
    for name in collection_names:
        bpy.data.collections.remove(bpy.data.collections[name])

    # in the case when you modify the world shader
    world_names = [world.name for world in bpy.data.worlds]
    for name in world_names:
        bpy.data.worlds.remove(bpy.data.worlds[name])
    # create a new world data block
    bpy.ops.world.new()
    bpy.context.scene.world = bpy.data.worlds["World"]

    purge_orphans()

def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

def rotate(point, angle_degrees, axis=(0,1,0)):
    theta_degrees = angle_degrees
    theta_radians = math.radians(theta_degrees)
    
    rotated_point = np.dot(rotation_matrix(axis, theta_radians), point)
    return rotated_point

clean_scene()

def get_calibration_matrix_K_from_blender(camd):
    f_in_mm = camd.lens
    scene = bpy.context.scene
    resolution_x_in_px = scene.render.resolution_x
    resolution_y_in_px = scene.render.resolution_y
    scale = scene.render.resolution_percentage / 100
    sensor_width_in_mm = camd.sensor_width
    sensor_height_in_mm = camd.sensor_height
    pixel_aspect_ratio = scene.render.pixel_aspect_x / scene.render.pixel_aspect_y
    if (camd.sensor_fit == 'VERTICAL'):
        # the sensor height is fixed (sensor fit is horizontal), 
        # the sensor width is effectively changed with the pixel aspect ratio
        s_u = resolution_x_in_px * scale / sensor_width_in_mm / pixel_aspect_ratio 
        s_v = resolution_y_in_px * scale / sensor_height_in_mm
    else: # 'HORIZONTAL' and 'AUTO'
        # the sensor width is fixed (sensor fit is horizontal), 
        # the sensor height is effectively changed with the pixel aspect ratio
        pixel_aspect_ratio = scene.render.pixel_aspect_x / scene.render.pixel_aspect_y
        s_u = resolution_x_in_px * scale / sensor_width_in_mm
        s_v = resolution_y_in_px * scale * pixel_aspect_ratio / sensor_height_in_mm

    # Parameters of intrinsic calibration matrix K
    alpha_u = f_in_mm * s_u
    alpha_v = f_in_mm * s_v
    u_0 = resolution_x_in_px*scale / 2
    v_0 = resolution_y_in_px*scale / 2
    skew = 0 # only use rectangular pixels

    K = Matrix(
        ((alpha_u, skew,    u_0),
        (    0  ,  alpha_v, v_0),
        (    0  ,    0,      1 )))
    return K



# import one model
car_object = bpy.ops.import_scene.gltf(filepath=path_to_glb_folder)
obj_focus = bpy.data.objects['Sketchfab_model']
bpy.context.object.display_type = 'TEXTURED'


#try white background
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 0.5)



# Add sun lamp
bpy.ops.object.light_add(type='SUN', align='WORLD', location=(0, 0, 500))

# Set sun lamp properties
sun = bpy.context.active_object.data
sun.energy = 0.1  # Adjust the intensity of the sunlight
sun.angle = 0.01  # Adjust the size of the sun disc



# Add area light at the same location as the camera
x = 10
bpy.ops.object.light_add(type='AREA', align='WORLD', location=(obj_focus.location.x+13*x, obj_focus.location.y+13*x, obj_focus.location.z + 1*x))
area_light = bpy.context.active_object.data
area_light.size = 7  # Set the size of the area light
area_light = bpy.context.active_object.data
area_light.energy = 100  # Set the energy of the area l

# Add track to constraint
bpy.ops.object.constraint_add(type='TRACK_TO')

# Set track to constraint target
bpy.context.object.constraints["Track To"].target = bpy.data.objects[1]

# initialize camera and tracking
bpy.ops.object.camera_add(location=(obj_focus.location.x+15*x, obj_focus.location.y+15*x, obj_focus.location.z + 5*x), 
                                rotation=(math.radians(90), 0, math.radians(45)))
camera = bpy.context.object
camera.data.lens = 20  # Set focal length to 20mm
bpy.ops.object.constraint_add(type='TRACK_TO') # set track 
bpy.context.object.constraints["Track To"].target = bpy.data.objects[2] 




# Set render settings
bpy.context.scene.render.image_settings.file_format = "JPEG"
# Adjust exposure and contrast in camera settings
bpy.context.scene.view_settings.view_transform = 'Filmic'
bpy.context.scene.view_settings.look = 'High Contrast'

# Set the number of samples for Cycles render engine
bpy.context.scene.cycles.samples = 500  # Adjust the number of rend
bpy.context.scene.eevee.taa_render_samples = 16
bpy.context.scene.render.resolution_x = 1024
bpy.context.scene.render.resolution_y = 1024  #set resolution of final pic



# Animate the camera in a circular motion
angle_increment = 360 / num_photos
for frame in range(num_photos):
    current_cam = camera.location
    new_cam = rotate(current_cam, angle_increment, axis=(0,0,1))
    camera.location = new_cam
#    area_light.location = new_cam
    
    bpy.context.scene.camera = bpy.context.view_layer.objects.active
    
    bpy.context.scene.frame_set(frame)
    
    print('!!!!!!!!!!')
    print(camera.location.x, camera.location.y, camera.location.z)


  # Render image for each frame
    glb_file = os.path.basename(path_to_glb_folder)
    bpy.context.scene.render.filepath = os.path.join(path_to_jpeg_folder, f"{glb_file.replace('.glb', '_')}_{frame + 1}.jpg")
    bpy.ops.render.render(write_still=True)

# Set the last frame to ensure the final state is captured
bpy.context.scene.frame_set(num_photos)




print(bpy.data.objects[1])


K = get_calibration_matrix_K_from_blender(bpy.data.objects['Camera'].data)
print(K)
                            
print(bpy.data.objects['Sketchfab_model'].location.x)





# List all glb files in the specified folder
#glb_file_list = [f for f in os.listdir(path_to_glb_folder) if f.lower().endswith('.glb')]

#for glb_file in glb_file_list:
#    # Import glb file
#    bpy.ops.import_scene.gltf(filepath=os.path.join(path_to_glb_folder, glb_file))

#    # Set up camera and light
#    bpy.ops.object.camera_add(location=(0, 0, 7), rotation=(math.radians(90), 0, math.radians(45)))
#    bpy.ops.object.light_add(type='POINT', location=(0, 0, 10))
#    
#    # Set render settings
#    bpy.context.scene.render.image_settings.file_format = "JPEG"

#    # Animate the camera in a circular motion
#    for frame in range(num_photos):
#        angle = frame * (2 * math.pi) / num_photos
#        bpy.context.object.location = (7 * math.cos(angle), 7 * math.sin(angle), 7)
#        bpy.context.scene.frame_set(frame + 1)
#        
#        # Render image for each frame
#        bpy.context.scene.render.filepath = os.path.join(path_to_jpeg_folder, f"{glb_file.replace('.glb', '_')}_{frame + 1}.jpg")
#        bpy.ops.render.render(write_still=True)

#    # Reset frame to 1 for the next glb file
#    bpy.context.scene.frame_set(1)

#clean_scene()
