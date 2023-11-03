import os
import argparse
import sys
from PIL import Image
import uuid
import json

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

def upscale_image_with_realesr(input_file, output_file, scale_factor):
    try:
        # run bash command on server side synchronously
        print("------bash command started------")
        os.system(f"python3 ../realesrgan/inference_realesrgan.py -n realesr-general-x4v3 -i ../supixel-toolkit/{input_file} -o ../supixel-toolkit/{output_file} --face_enhance -s {scale_factor}")
        print("------bash command finished------")
        print(f"Image {input_file} upscaled by {scale_factor}X and saved to {output_file}")
    except Exception as e:
        print(f"Error: {str(e)}")

def make_obfuscared_pair(real_folder, generated_folder, output_folder):
    try:
        os.makedirs(output_folder, exist_ok=True)
        json_file = []  # Create an empty list to store image data
        for filename in os.listdir(real_folder):
            real_path = os.path.join(real_folder, filename)
            generated_path = os.path.join(generated_folder, filename)

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
    parser.add_argument("--reverse-generate", default=False, help="Run realesr generator on the output folder")
    parser.add_argument("--generate-pair", default=False, help="Generate obfuscared pair")
    args = parser.parse_args()

    if not args.input or not args.output or not args.scale:
        print("Missing required arguments")
        sys.exit(1)
    
    input_folder = args.input
    output_folder = args.output
    scale_factor = args.scale
    extensions = args.extensions.split(",")
    reverse_generate = args.reverse_generate

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

    if reverse_generate:
        # make the output folder if it doesn't exist
        output_folder = os.path.join(output_folder, "_upscaled")
        os.makedirs(output_folder, exist_ok=True)
        for filename in os.listdir(output_folder):
            path = os.path.join(output_folder, filename)
            if os.path.isfile(path):
                _, file_extension = os.path.splitext(path)
                if file_extension.lower() in extensions:
                    output_path = os.path.join(output_folder, filename)
                    output_path = output_path.replace(" ", "_")
                    upscale_image_with_realesr(path, output_path, 1/scale_factor)

        if args.obfuscate:
            # make obfuscared folder 
            upscaled_folder = os.path.join(output_folder, "_upscaled")
            obfuscared_folder = os.path.join(output_folder, "_obfuscared")
            os.makedirs(obfuscared_folder, exist_ok=True)
            make_obfuscared_pair(output_folder, upscaled_folder, obfuscared_folder)


