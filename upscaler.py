import os
import argparse
import sys
from PIL import Image
import uuid
import json

def upscale_image_with_realesr(input_file, output_folder, scale_factor):
    try:
        # run bash command on server side synchronously
        print("------bash command started------")
        os.system(f"python3 ../realesrgan/inference_realesrgan.py -n realesr-general-x4v3 -i ../supixel-toolkit/{input_file} -o ../supixel-toolkit/{output_folder} --face_enhance -s {scale_factor}")
        print("------bash command finished------")
        print(f"Image {input_file} upscaled by {scale_factor}X and saved to {output_folder}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upscale images in a folder.")
    parser.add_argument("-i", "--input", help="Input folder containing images")
    parser.add_argument("-o", "--output", help="Output folder to save upscaled pair images")
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

    generated_folder = output_folder
    os.makedirs(generated_folder, exist_ok=True)
    for filename in os.listdir(input_folder):
        path = os.path.join(input_folder, filename)
        if os.path.isfile(path):
            _, file_extension = os.path.splitext(path)
            if file_extension.lower() in extensions:
                upscale_image_with_realesr(path, generated_folder, 1/scale_factor)