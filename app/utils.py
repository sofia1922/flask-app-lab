import os
import secrets
from PIL import Image
from flask import current_app

def save_profile_image(image_file):
    random_hex = secrets.token_hex(8)
    ext = image_file.filename.split('.')[-1]
    filename = f"{random_hex}.{ext}"

    img_folder = os.path.join(current_app.root_path, "static/images")
    full_path = os.path.join(img_folder, filename)

    image_file.save(full_path)

    img = Image.open(image_file)
    img.thumbnail((128, 128))

    thumb_path = os.path.join(img_folder, f"thumb_{filename}")
    img.save(thumb_path)

    return filename
