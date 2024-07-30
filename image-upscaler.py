from pathlib import Path
import glob
import os
from PIL import Image
import requests
import sys


def downloadImages(clear_cache):
    # Clear existing images
    if clear_cache:
        files = glob.glob("title-images/*.png")
        for f in files:
            os.remove(f)

    # Find manifest URLs
    json = requests.get("https://bungie.net/Platform/Destiny2/Manifest").json()
    records_url = json["Response"]["jsonWorldComponentContentPaths"]["en"][
        "DestinyRecordDefinition"
    ]
    presentation_node_url = json["Response"]["jsonWorldComponentContentPaths"]["en"][
        "DestinyPresentationNodeDefinition"
    ]

    # Get data
    try:
        records = requests.get(f"https://bungie.net{records_url}").json()
    except:
        print(
            "Could not get Manifest: either not connected to the internet or you are being rate-limited"
        )
        sys.exit(1)
    presentation_nodes = requests.get(
        f"https://bungie.net{presentation_node_url}"
    ).json()

    # Find all records with associated titles
    records_with_titles = set()
    for data in records.values():
        if not data.get("titleInfo") or not data["titleInfo"]["hasTitle"]:
            continue

        if not data.get("displayProperties") or not data["displayProperties"]["name"]:
            continue

        hash = data["hash"]
        name = data["displayProperties"]["name"]
        description = data["displayProperties"]["description"]
        title = data["titleInfo"]["titlesByGender"]["Male"]

        print("Record")
        print("  > Hash:", hash)
        print("  > Name:", name)
        print("  > Description:", description)
        print("  > Title:", title)
        records_with_titles.add(hash)

    # Find all presentation nodes that match one of these titles
    images_to_download = []
    for data in presentation_nodes.values():
        completion_record_hash = data.get("completionRecordHash")
        if (
            not completion_record_hash
            or completion_record_hash not in records_with_titles
        ):
            continue

        hash = data["hash"]
        name = data["displayProperties"]["name"]
        description = data["displayProperties"]["description"]
        title = records[f"{completion_record_hash}"]["titleInfo"]["titlesByGender"][
            "Male"
        ]

        icon = data["displayProperties"]["icon"]
        gold_icon = data["displayProperties"]["iconSequences"][0]["frames"][2]
        silver_icon = data["displayProperties"]["iconSequences"][1]["frames"][2]

        print("Presentation Node")
        print("  > Hash:", hash)
        print("  > Name:", name)
        print("  > Description:", description)
        print("  > Associated Title:", title)
        print("  > Icon:", icon)
        print("  > Gold Icon:", gold_icon)
        print("  > Silver Icon:", silver_icon)

        images_to_download.append(
            {"title": title, "tag": "", "image_url": f"https://bungie.net{icon}"}
        )
        images_to_download.append(
            {
                "title": title,
                "tag": "-gold",
                "image_url": f"https://bungie.net{gold_icon}",
            }
        )
        images_to_download.append(
            {
                "title": title,
                "tag": "-silver",
                "image_url": f"https://bungie.net{silver_icon}",
            }
        )
    print()

    # Download images
    for image_to_download in images_to_download:
        title = image_to_download["title"]
        tag = image_to_download["tag"]
        filename = f"title-images/{title}{tag}.png"
        image_url = image_to_download["image_url"]

        if Path(filename).exists():
            continue

        img_data = requests.get(image_url).content
        with open(filename, "wb") as handler:
            handler.write(img_data)

    return list(
        map(
            lambda data: {
                "title": data["title"],
                "tag": data["tag"].replace("-", ""),
                "filename": filename,
            },
            images_to_download,
        )
    )


def upscaleImages(images):
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


def main():
    original_images = downloadImages(False)

    upscaled_images = upscaleImages(original_images)

    # vector_images = vectorizeImages(upscaled_images)


if __name__ == "__main__":
    main()
