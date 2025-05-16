Version = [0,0,1]
State = "SCR"

import os
from PIL import Image

def convert_webp_to_png(directory):
    """Converts all .webp images in the given directory to .png and saves them in a 'Converted' folder."""
    
    # Ensure the directory exists
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return
    
    # Create the 'Converted' folder if it doesn't exist
    converted_dir = os.path.join(directory, "Converted")
    os.makedirs(converted_dir, exist_ok=True)

    # Loop through all files in the directory
    for filename in os.listdir(directory):
        if filename.lower().endswith(".webp"):
            webp_path = os.path.join(directory, filename)
            png_filename = f"{os.path.splitext(filename)[0]}.png"
            png_path = os.path.join(converted_dir, png_filename)

            try:
                # Open and convert image
                with Image.open(webp_path) as img:
                    img.save(png_path, "PNG")
                print(f"Converted: {webp_path} -> {png_path}")
            except Exception as e:
                print(f"Failed to convert {webp_path}: {e}")

if __name__ == "__main__":
    target_directory = input("Enter the target directory: ").strip()
    convert_webp_to_png(target_directory)
