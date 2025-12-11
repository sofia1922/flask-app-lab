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

def save_recipe_image(image_file):
    import os, secrets
    from PIL import Image
    from flask import current_app

    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(image_file.filename)
    filename = random_hex + ext.lower()

    folder = os.path.join(current_app.root_path, "static/recipes")
    os.makedirs(folder, exist_ok=True)

    full_path = os.path.join(folder, filename)
    image_file.save(full_path)

    img = Image.open(full_path)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    img_big = img.copy()
    img_big.thumbnail((1000, 1000))
    img_big.save(full_path)

    thumb_path = os.path.join(folder, f"thumb_{filename}")
    img_thumb = img.copy()
    img_thumb.thumbnail((300, 300))
    img_thumb.save(thumb_path)

    return filename