import os
from pathlib import Path
from PIL import Image


def scale_setter(prompt):

    while True:
        try:
            scale = int(input(prompt))
            return scale
        except ValueError:
            print("INVALID INPUT. INTEGER ANSWERS ONLY.")
            continue


def y_or_n(prompt):

    answers = {"Y": True, "N": False}
    while True:
        ans = input(prompt).upper()
        if ans in [*answers]:
            return answers[ans]
        else:
            print("INVALID INPUT. (Y/N) ANSWERS ONLY.")
            continue


def main(file_path, bulk, gosub_folder=True, scale="50"):

    print("Going Through: ")
    print(file_path)
    patterns = ("*.jpg", "*.png", "*.gif", "*.jpeg")
    destination = Path(file_path.parent / "RESIZED_PHOTOS")
    destination.mkdir(parents=True, exist_ok=True)
    if gosub_folder:
        img_files = Path.rglob(file_path, "*")
    else:
        img_files = Path.glob(file_path, "*")
    for img in img_files:
        if any(img.match(pat) for pat in patterns):
            pic_name = img.name
            print(img)
            if bulk == False:
                scale = scale_setter("Resize image by (%): ")
                pic = Image.open(img)
                x = int(round(pic.size[0] * 0.01 * scale))
                y = int(round(pic.size[1] * 0.01 * scale))
                new_pic = pic.resize((x, y))
                image_at = Path(destination / pic_name)
                new_pic.save(image_at)
                os.startfile(image_at)
            else:
                pic = Image.open(img)
                x = int(round(pic.size[0] * 0.01 * scale))
                y = int(round(pic.size[1] * 0.01 * scale))
                new_pic = pic.resize((x, y))
                image_at = Path(destination / pic_name)
                new_pic.save(image_at)
                os.startfile(destination)
    print("\n\nYou can find the resized images at: " + str(destination))


if __name__ == "__main__":
    file_path = Path.cwd()
    scale = "50"

    gosub_folder = y_or_n("Resize the files in the sub folders?(Y/N): ")

    bulk = y_or_n("Resize all files as a group?(Y/N): ")
    if bulk:
        scale = scale_setter("Resize all images by (%): ")
        pass
    else:
        pass

    main(file_path=file_path, bulk=bulk, scale=scale, gosub_folder=gosub_folder)

    print("""\n\n
MIT License

Copyright (c) 2026 Sanjay S
""")
    input("\n\nPress Enter to close....")
