# <!-- [SS-0]: Meta Data -----> #
VERSION = '0.2.29'
DATE = '5.5.25'
DESC = 'Convert Images to ICO Format'
DEV = 'AngrySatan666'

# <!-- [SS-1]: Imports -----> #
import os, sys
from PIL import Image
import shutil
import time
import argparse

# <!-- [SS-2]: Global Variables -----> #
_dir = None
work_dir = None
done_dir = None
dest = ("G:\\My Drive\\Icons\\ico")
icon_sizes = [(256, 256), (128, 128), (96,96), (64, 64), (48,48), (40,40), (32, 32), (24,24), (20,20), (16, 16)]

# <!-- [SS-3]: Snippet Functions -----> #
def info (*args) :
    for txt in args :
        print (f"[INFO] {txt}")
        print (" ")

def warn (*args) :
    for txt in args :
        print (f"[WARN] {txt}")
        print (" ")

def error (*args) :
    for txt in args :
        print (f"[ERROR] {txt}")
        print (" ")

def timer (x) :
    while x > 0 :
        print (x)
        print (" ")
        time.sleep (1)
        x -= 1

def base (work=None, output=None) :
    global _dir, work_dir, done_dir
    _dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if work is None or work == "" :
        work_dir = os.path.join(_dir, 'static', 'img')
        os.makedirs(work_dir, exist_ok=True)
    elif work is not None or work != "" :
        work_dir = work
    if output is None :
        done_dir = os.path.join(_dir, 'static', 'img', 'done')
        os.makedirs(done_dir, exist_ok=True)
    elif output is not None and output != "" :
        done_dir = output
    os.makedirs(done_dir, exist_ok=True)

# <!-- [SS-4]: Script Functions -----> #
def prepare (bugs=bool) :
    if bugs is True :
        info("Converting image files to PNG...")
    for filename in os.listdir(work_dir):
        if filename.lower().endswith((".webp", ".jpg", ".jpeg")):
            img_path = os.path.join(work_dir, filename)
            png_filename = f"{os.path.splitext(filename)[0]}.png"
            png_path = os.path.join(work_dir, png_filename)
            try:
                with Image.open(img_path) as img:
                    img.save(png_path, "PNG")
                if bugs is True :
                    info(f"Converted {img_path} to PNG: {png_path}")
            except Exception as e :
                error(f"Failed to convert {img_path}: {e}")
    if bugs is True :
        info("All images converted to .png format")

def optimize (img_path, bugs=bool) :
    info(f"Clearing {img_path} metadata...")
    try :
        with Image.open(img_path) as img :
            img.info.clear()
            img.save(img_path, "PNG", optimize=True)
            if bugs is True :
                info(f"Metadata cleared for {img_path}")
    except Exception as e :
        if bugs is True :
            error(f"Failed to clear {img_path} metadata: {e}")

def move (bugs=bool) :
    if "--ico" in sys.argv :
        if bugs is True :
            info("Moving icons to the designated folder")
        for filename in os.listdir(done_dir) :
            if filename.lower().endswith(".ico") :
                icon = os.path.join(done_dir, filename)
                dest_path = os.path.join(dest, filename)
                try :
                    shutil.move(icon, dest_path)
                    if bugs is True :
                        info(f"Moved {filename} to {dest}")
                except Exception as e :
                    if bugs is True :
                        error(f"Failed to move {filename} to {dest}: {e}")
        if bugs is True:
            info("Icon moving complete")

def png_ico (work=None, output=None, bugs=bool) :
    base (work=work, output=output)
    if not any(f.lower().endswith((".webp", ".jpg", ".jpeg", ".png", ".ico")) for f in os.listdir(work_dir)):
        if bugs is True :
            warn("No convertible images found in work_dir, listing contents, then exiting")
            warn("Files detected in work_dir:", os.listdir(work_dir))
        timer (5)
        exit ()
    prepare (bugs=bugs)
    if bugs is True :
        info("Converting any .ico to .png")
    for filename in os.listdir(work_dir) :
        if filename.lower().endswith(".ico") :
            if bugs is True :
                info (f"Converting {filename} to .png")
            path = os.path.join(work_dir, filename)
            try :
                with Image.open(path) as img :
                    allsizes = img.info.get("sizes", [])
                    if allsizes:
                        largest = max(allsizes, key=lambda s: s[0])
                    else:
                        largest = img.size
                    png_path = os.path.join(work_dir, os.path.splitext(os.path.basename(path))[0] + ".png")
                    img.resize(largest, Image.LANCZOS).save(png_path, format="PNG")
                    if bugs is True :
                        info(f"Icon {filename} converted to png", "Deleting the .ico")
                    os.remove(path)
                    if bugs is True :
                        info(f"The .ico was removed")
            except Exception as e :
                if bugs is True :
                    error(f"Error processing icon {filename}: {e}")
    if bugs is True :
        info("Creating the .ico icons...")
    for filename in os.listdir(work_dir) :
        if filename.lower().endswith(".png") :
            png_path = os.path.join(work_dir, filename)
            optimize (png_path, bugs=bugs)
            ico_path = os.path.join(done_dir, os.path.splitext(filename)[0] + ".ico")
            try :
                image = Image.open(png_path)
                image.save(ico_path, format="ICO", sizes=icon_sizes)
                if bugs is True :
                    info(f"Converted: {filename} to an ico at : {ico_path}")
                    info("Removing .png...")
                os.remove(png_path)
                if bugs is True :
                    info(".png removed")
            except Exception as e :
                if bugs is True :
                    error(f"Error processing {filename}: {e}")
    if bugs is True :
        info("Conversion process completed!")
    move (bugs=bugs)

# <!-- [SS-5]: Run -----> #
if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description="Convert Images to ICO format.")
    parser.add_argument('--work', type=str, help="Directory Path to Images to Convert")
    parser.add_argument('--output', type=str, help="Output Directory for Converted Icons")
    parser.add_argument('--bugs', action='store_true', help="Enable Debugging Messages")
    args = parser.parse_args()
    if args.bugs:
        info("Debugging mode enabled")
        bugs = True
    elif not args.bugs:
        bugs = False
    png_ico (bugs=bugs)
