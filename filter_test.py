import os  # libs needed for car filtration
import sys
from pathlib import Path
from typing import Tuple

import cv2
import numpy as np
import matplotlib.pyplot as plt
from openvino.runtime import Core

sys.path.append("../utils")
import notebook_utils as utils



# A directory where the model will be downloaded.
base_model_dir = "model"
# The name of the model from Open Model Zoo.
detection_model_name = "vehicle-detection-0200"
recognition_model_name = "vehicle-attributes-recognition-barrier-0039"
# Selected precision (FP32, FP16, FP16-INT8)
precision = "FP32"

# Check if the model exists.
detection_model_path = (
    f"model/intel/{detection_model_name}/{precision}/{detection_model_name}.xml"
)
recognition_model_path = (
    f"model/intel/{recognition_model_name}/{precision}/{recognition_model_name}.xml"
)

# Download the detection model.
if not os.path.exists(detection_model_path):
    download_command = f"omz_downloader " \
                       f"--name {detection_model_name} " \
                       f"--precision {precision} " \
                       f"--output_dir {base_model_dir}"
    print('1')
#  ! $download_command
# Download the recognition model.
if not os.path.exists(recognition_model_path):
    download_command = f"omz_downloader " \
                       f"--name {recognition_model_name} " \
                       f"--precision {precision} " \
                       f"--output_dir {base_model_dir}"
    print('2')

    ! @download_command


