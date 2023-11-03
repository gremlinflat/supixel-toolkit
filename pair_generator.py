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

def make_obfuscared_pair(real_folder, generated_folder, output_folder):
    print("------make_obfuscared_pair------")
    print("real_folder: ", real_folder)
    print("generated_folder: ", generated_folder)
    print("output_folder: ", output_folder)
    print("------make_obfuscared_pair------")
    try:
        os.makedirs(output_folder, exist_ok=True)
        json_file = []  # Create an empty list to store image data
        for filename in os.listdir(real_folder):
            real_path = os.path.join(real_folder, filename)
            
            # add _out in generated filename before extension
            f_gen, f_ext_gen = os.path.splitext(filename)
            f_gen += "_out" + f_ext_gen
            generated_path = os.path.join(generated_folder, f_gen)

            if os.path.isfile(real_path) and os.path.isfile(generated_path):
                # get filename extension
                _, file_extension = os.path.splitext(real_path)

                # Generate a unique filename using UUID
                new_real_filename = str(uuid.uuid4()) + file_extension
                new_generated_filename = str(uuid.uuid4()) + file_extension

                # copy and rename those two files into output folder
                new_real_path = os.path.join(output_folder, new_real_filename)
                new_generated_path = os.path.join(output_folder, new_generated_filename)

                os.system(f"cp {real_path} {new_real_path}")
                os.system(f"cp {generated_path} {new_generated_path}")

                # Create data dictionary for JSON
                image_data = {
                    "real": f"{new_real_filename}",  # Replace with actual URL or path
                    "generated": f"{new_generated_filename}",  # Replace with actual URL or path
                }
                json_file.append(image_data)

        # Create JSON structure
        json_data = {"data": json_file}

        # Write JSON to a file
        with open("output.json", "w") as json_file:
            json.dump(json_data, json_file, indent=2)

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
    scale_factor = args.scale
    extensions = args.extensions.split(",")

    generated_folder = input_folder + "_upscaled_by_ai"
    os.makedirs(generated_folder, exist_ok=True)
    for filename in os.listdir(input_folder):
        path = os.path.join(input_folder, filename)
        if os.path.isfile(path):
            _, file_extension = os.path.splitext(path)
            if file_extension.lower() in extensions:
                upscale_image_with_realesr(path, generated_folder, 1/scale_factor)

    obfuscared_folder = input_folder + "_obfuscared"
    os.makedirs(obfuscared_folder, exist_ok=True)         
    make_obfuscared_pair(input_folder, generated_folder, obfuscared_folder)