import prompt
from prompt import Question
from prompt import startfile
from pathlib import Path
from PIL import Image

def main(in_path, out_path, bulk, gosub_folder=True, scale='50'):

    prompt.title(prompt="Going Through: ")
    prompt.title(prompt=in_path)
    

    def resize(img,scale,destination,pic_name):
        pic = Image.open(img)
        x = int(round(pic.size[0]*0.01*scale))
        y = int(round(pic.size[1]*0.01*scale))
        if scale <= 100:
            new_pic = pic.resize((x,y), 1)
        elif scale > 100:
            new_pic = pic.resize((x,y), 3)
        image_at = Path(destination / pic_name)
        
        try:
            new_pic.save(image_at)
            startfile(destination)
        except PermissionError:
            prompt.warning(prompt="You do not have permission to save at " + str(destination) + "\nPlease Restart the Program")

    patterns = ("*.jpg", "*.png", "*.gif","*.jpeg")
    destination = Path(out_path)
    destination.mkdir(parents=True,exist_ok=True)

    if gosub_folder:
        img_files = Path.rglob(in_path,'*') #Checks for all files in subfolders too
    else:
        img_files = Path.glob(in_path,'*')
        
    for img in img_files:
        if any(img.match(pat) for pat in patterns):
            pic_name = img.name
            prompt.see(prompt=img)

            if bulk == False:
                scale = Question("Resize all images by(%)?: ", "Invalid Answer Enter Integer Answers Only")
                scale = scale.scale_setter()
            elif bulk == True:
                pass

            resize(img,scale,destination,pic_name)

            
    prompt.title(prompt="\n\nYou can find the resized images at: " + str(destination)+"\n")

while True:
    in_path = Question("Which Folder has the images?: ", "The Path doesn't exist or You don't have Permission to Access it")
    in_path = in_path.ask_destination()

    bulk = Question("Do you want to resize all the images at once? (Y/N): ")
    bulk = bulk.y_or_no()

    if bulk:
        scale = Question("Resize all images by(%)?: ", "Invalid Answer Enter Integer Answers Only")
        scale = scale.scale_setter()
    elif bulk == False:
        scale = None

    gosub_folder  = Question("Resize the files in the sub folders?(Y/N): ")
    gosub_folder = gosub_folder.y_or_no()

    out_path = Question("Where to save the images?: ")
    out_path = out_path.ask_destination()

    if out_path.is_relative_to(in_path):
        prompt.warning("Output Path is a subfolder")
        print("")
        continue
    elif out_path.is_relative_to(in_path) == False:
        break


main (in_path=in_path,bulk=bulk,scale=scale,gosub_folder=gosub_folder,out_path=out_path)



prompt.subtle(prompt='''\n\n
MIT License

Copyright (c) 2026 Sanjay S
''')

input("\n\nPress Enter to close....")