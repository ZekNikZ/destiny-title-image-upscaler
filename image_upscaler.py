def upscale_images(images):
    for image in images:
        title = image["title"]
        tag = image["tag"]
        input_filename = image["filename"]
        output_filename = image["filename"].replace("title-images/", "upscaled-images/")

        print("Image Upscaling")
        print(f"  > Title: {title}")
        print(f"  > Tag: {tag}")
        print(f"  > Original File: {input_filename}")
        print(f"  > Upscaled File: {output_filename}")
    print()
