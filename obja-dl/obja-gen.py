import bpy
import os

path_to_glb_folder = "/data/waffle1/crawl/objaverse/hf-objaverse-v1/glbs/000-000/" # If you are using Windows use r"\Users\Path\To\Folder"
path_to_jpeg_folder = "/data/waffle1/crawl/objaverse/images/"

def deleteAllObjects():
    """
    Deletes all objects in the current scene
    """
    deleteListObjects = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'HAIR', 'POINTCLOUD', 'VOLUME', 'GPENCIL',
                         'ARMATURE', 'LATTICE', 'EMPTY', 'LIGHT', 'LIGHT_PROBE', 'CAMERA', 'SPEAKER']

    # Select all objects in the scene to be deleted:

    for o in bpy.context.scene.objects:
        for i in deleteListObjects:
            if o.type == i:
                o.select_set(False)
            else:
                o.select_set(True)
    bpy.ops.object.delete() # Deletes all selected objects in the scene

deleteAllObjects()

glb_dirList = os.listdir(path_to_glb_folder)

removeList = [".gitignore", ".DS_Store"] # If you have . files in your directory
glb_dirList = [x for x in glb_dirList if (x not in removeList)]

for i in glb_dirList:
    bpy.ops.import_scene.gltf(filepath=os.path.join()) # Import .glb file to scene

    bpy.context.scene.render.filepath = path_to_jpeg_folder # Set save path for images
    bpy.context.scene.render.image_settings.file_format = "JPEG" # Set image file format
    bpy.ops.render.render(write_still=True) # Tell Blender to render an image

    deleteAllObjects()