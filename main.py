from ntpath import exists, isfile

import prompt
from prompt import Question
from prompt import startfile
from pathlib import Path
from PIL import Image


def resizer(in_path, out_path, bulk, gosub_folder=True, scale="50"):

    prompt.title(prompt="Going Through: ")
    prompt.title(prompt=in_path)
    prompt.see(prompt="Resizing... ")

    def resize(img, scale, destination, pic_name):
        pic = Image.open(img)
        x = int(round(pic.size[0] * 0.01 * scale))
        y = int(round(pic.size[1] * 0.01 * scale))
        if scale <= 100:
            new_pic = pic.resize((x, y), 1)  # better quality for downsized images
        elif scale > 100:
            new_pic = pic.resize((x, y), 3)  # better quality for upsize images

        pic_name = Path("RESIZED_" + pic_name)
        image_at = Path(destination / pic_name)

        try:
            new_pic.save(image_at)
            if bulk == False:
                startfile(destination / pic_name)
            elif bulk == True:
                pass
        except PermissionError:
            prompt.warning(
                prompt="You do not have permission to save at "
                + str(destination)
                + "\nPlease Restart the Program"
            )

    patterns = ("*.jpg", "*.png", "*.gif", "*.jpeg")
    destination = Path(out_path)
    try:
        destination.mkdir(parents=True, exist_ok=True)
    except OSError:
        prompt.warning("given input path doesn't exist! Restarting program...")
        main()
        return None

    if gosub_folder:
        img_files = Path.rglob(in_path, "*")  # Checks for all files in subfolders too
    else:
        img_files = Path.glob(in_path, "*")

    for img in img_files:
        if any(img.match(pat) for pat in patterns):
            pic_name = img.name
            prompt.see(prompt=img)

            if bulk == False:
                scale = Question(
                    "Resize image by(%)?: ",
                    "Invalid Answer Enter Integer Answers Only",
                )
                scale = scale.scale_setter()
            elif bulk == True:
                pass

            resize(img, scale, destination, pic_name)

    prompt.title(
        prompt="\n\nYou can find the resized images at: " + str(destination) + "\n"
    )

    startfile(destination)


def main():
    while True:

        prompt.warning("press ctrl+C to terminate program anytime")
        in_path = Question(
            "Which Folder has the images? Leave empty to use folder where program is saved: ",
            "The Path doesn't exist or You don't have Permission to Access it",
        )
        in_path = in_path.ask_destination()

        if in_path == Path(""):
            in_path = Path.cwd()
            break
        else:
            if in_path.exists() == True:
                if in_path.is_file():
                    prompt.warning("It is a file path! give a folder path!")
                    continue
                else:
                    break
            elif in_path.exists() == False:
                prompt.warning("Path Doesn't Exist! Give A Valid file path")
                continue

    bulk = Question("Do you want to resize all the images at once? (Y/N): ")
    bulk = bulk.y_or_no()

    if bulk:
        scale = Question(
            "Resize all images by(%)?: ", "Invalid Answer Enter Integer Answers Only"
        )
        scale = scale.scale_setter()
    elif bulk == False:
        scale = None

    gosub_folder = Question("Resize the files in the sub folders?(Y/N): ")
    gosub_folder = gosub_folder.y_or_no()

    while True:

        out_path = Question(
            "Where to save the images? Leave it empty to save files outside input folder: "
        )
        out_path = out_path.ask_destination()

        if out_path == Path(""):
            out_path = Path(in_path.parent / "RESIZED_PHOTOS")
            break
        else:
            if out_path.is_relative_to(in_path):
                prompt.warning("Output Path is a subfolder")
                print("")
                continue
            elif out_path.is_relative_to(in_path) == False:
                break

    resizer(
        in_path=in_path,
        bulk=bulk,
        scale=scale,
        gosub_folder=gosub_folder,
        out_path=out_path,
    )


main()  # runs the entire thing


prompt.subtle(prompt="\n\nMIT License\nCopyright (c) 2026 Sanjay S")

input("\n\nPress Enter to close....")
