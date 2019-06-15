import base64
import os
from io import BytesIO
from PIL import Image


def image_to_base64(image_path):
    img = Image.open(image_path)
    img = resize(img)
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data).decode('utf-8')
    return base64_str


def resize(img):
    std_width = 250
    std_height = 250
    width, height = img.size
    print(width, height)
    if width < std_width and height < std_height:
        return img
    new_width = width
    new_height = height
    while new_width > std_width or new_height > std_height:
        new_width *= 0.9
        new_height *= 0.9
    new_width = int(new_width)
    new_height = int(new_height)
    print(new_width, new_height)
    return img.resize((new_width, new_height))
