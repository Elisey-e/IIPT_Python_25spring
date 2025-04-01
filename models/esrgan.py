import numpy as np
import torch
from PIL import Image
from RealESRGAN import RealESRGAN

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = RealESRGAN(device, scale=2)
model.load_weights('weights/RealESRGAN_x2.pth', download=True)

def neural_network_upscale(image : Image) -> np.array:
    """Upscale image using RealESRGAN model."""
    sr_image = model.predict(image)
    return np.array(sr_image)