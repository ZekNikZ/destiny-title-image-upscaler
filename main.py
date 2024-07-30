from image_downloader import download_images
from image_upscaler import upscale_images


def main():
    original_images = download_images(False)

    upscaled_images = upscale_images(original_images)

    # vector_images = vectorizeImages(upscaled_images)


if __name__ == "__main__":
    main()
