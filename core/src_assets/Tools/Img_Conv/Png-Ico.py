Version = [0,0,1]
State = "SCR"

import os
from PIL import Image

# Define the target directory containing PNGs
target_directory = "C:\\Users\\angry\\Pictures\\Icons\\NotCons"  # Change this to your folder containing PNGs

# Define output directory within the target directory
ico_directory = os.path.join(target_directory, "Ico")
os.makedirs(ico_directory, exist_ok=True)  # Ensure the directory exists

# Define icon sizes
icon_sizes = [(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)]

# Process each PNG file in the target directory
for filename in os.listdir(target_directory):
    if filename.lower().endswith(".png"):
        png_path = os.path.join(target_directory, filename)
        ico_path = os.path.join(ico_directory, os.path.splitext(filename)[0] + ".ico")

        try:
            # Open the image and convert it to ICO
            image = Image.open(png_path)
            image.save(ico_path, format="ICO", sizes=icon_sizes)
            print(f"Converted: {filename} -> {ico_path}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

print("Conversion process completed!")