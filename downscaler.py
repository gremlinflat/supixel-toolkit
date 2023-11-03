import os
import argparse
import sys
from PIL import Image

def downscale_image(input_file, output_file, scale_factor):
    try:
        with Image.open(input_file) as img:
            width, height = img.size
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            
            resized_img = img.resize((new_width, new_height))
            resized_img.save(output_file)
            print(f"Downscaled {input_file} to {new_width}x{new_height} and saved to {output_file}")
    except Exception as e:
        print(f"Error: {str(e)}")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Downscale images in a folder.")
    parser.add_argument("-i", "--input", help="Input folder containing images")
    parser.add_argument("-o", "--output", help="Output folder to save downscaled images")
    parser.add_argument("-s", "--scale", type=float, help="Scale factor (e.g., 0.4 for 40%)")
    parser.add_argument("-e", "--extensions", default=".jpg,.jpeg,.png", help="Comma-separated list of image extensions")
    args = parser.parse_args()

    if not args.input or not args.output or not args.scale:
        print("Missing required arguments")
        sys.exit(1)
    
    input_folder = args.input
    output_folder = args.output
    scale_factor = args.scale
    extensions = args.extensions.split(",")

    # make the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        path = os.path.join(input_folder, filename)
        if os.path.isfile(path):
            _, file_extension = os.path.splitext(path)
            if file_extension.lower() in extensions:
                output_path = os.path.join(output_folder, filename)
                output_path = output_path.replace(" ", "_")
                downscale_image(path, output_path, scale_factor)