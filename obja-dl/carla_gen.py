import carla
import random
import math
import os

# Connect to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

# Load a CARLA world and retrieve the blueprint library
world = client.get_world()
blueprint_library = world.get_blueprint_library()

# Output directory for generated images
output_folder = '~/Picture/carla_gen'
os.makedirs(output_folder, exist_ok=True)

# Parameters
num_models_per_base = 5  # Number of models to generate for each base model
azimuth_angle = 0.0  # Fixed azimuth angle for image capture
angle_interval = 10.0  # Angle interval for capturing images

# Function to set random texture and color for a vehicle
def set_random_attributes(vehicle):
    # Set random texture (if applicable)
    if 'color' in vehicle.attributes:
        vehicle.set_attribute('color', f'{random.randint(0, 255)},{random.randint(0, 255)},{random.randint(0, 255)}')
    
    # Set random color (if applicable)
    if 'color' in vehicle.attributes:
        vehicle.set_attribute('color', f'{random.randint(0, 255)},{random.randint(0, 255)},{random.randint(0, 255)}')

# Function to capture and save images for a vehicle
def capture_images(vehicle):
    # Spawn a camera on the vehicle
    camera_transform = carla.Transform(carla.Location(x=-5.5, z=2.8), carla.Rotation(pitch=-15))
    camera = world.spawn_actor(blueprint_library.find('sensor.camera.rgb'), camera_transform, attach_to=vehicle)

    # Capture images at different angles
    for angle in range(0, 360, int(angle_interval)):
        world.tick()
        camera.set_transform(camera_transform)
        camera.listen(lambda image: image.save_to_disk(os.path.join(output_folder, f'image_{vehicle.id}_{angle}.png')))

    # Destroy the camera
    camera.destroy()

# Iterate through each vehicle base model
for vehicle_bp in blueprint_library.filter('vehicle'):
    # Spawn multiple instances of the base model
    for _ in range(num_models_per_base):
        # Spawn the vehicle at a random location
        spawn_point = carla.Transform(carla.Location(x=random.uniform(-50, 50), y=random.uniform(-50, 50), z=2))
        vehicle = world.spawn_actor(vehicle_bp, spawn_point)

        # Set random attributes for the vehicle
        set_random_attributes(vehicle)

        # Capture and save images for the vehicle
        capture_images(vehicle)

        # Destroy the vehicle
        vehicle.destroy()
