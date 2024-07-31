import glob
import os
from pathlib import Path
import torch
from PIL import Image


def upscale_images(images, clear_cache=False):
    # Clear existing images
    if clear_cache:
        files = glob.glob("upscaled-images/*.png")
        for f in files:
            os.remove(f)

    # Create model
    model = torch.hub.load(
        "nagadomi/nunif:master",
        "waifu2x",
        model_type="art_scan",
        device_ids=[0],
        method="scale4x",
        noise_level=3,
        tile_size=256,
        batch_size=4,
        # keep_alpha=False,
        trust_repo=True,
    ).to("cuda")

    # Generate each image
    for image in images:
        title = image["title"]
        tag = image["tag"]
        input_filename = image["filename"]
        output_filename = image["filename"].replace("title-images/", "upscaled-images/")

        if not Path(output_filename).exists():
            # Upscale the image
            input_image = Image.open(input_filename).convert("RGBA")
            result = model.infer(input_image)
            result.save(output_filename)

        print("Image Upscaling")
        print(f"  > Title: {title}")
        print(f"  > Tag: {tag}")
        print(f"  > Original File: {input_filename}")
        print(f"  > Upscaled File: {output_filename}")
    print()
