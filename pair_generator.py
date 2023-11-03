import os
import argparse
import sys
from PIL import Image
import uuid
import json

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
    parser = argparse.ArgumentParser(description="obfuscate pair of image in a folder.")
    parser.add_argument("-ir", "--inputr", help="Input folder containing real images")
    parser.add_argument("-ig", "--inputg", help="Input folder containing generated images")
    parser.add_argument("-o", "--output", help="Output folder to save obfuscated pair images")
    args = parser.parse_args()

    if not args.inputr or not args.inputg or not args.output:
        print("Missing required arguments")
        sys.exit(1)
    
    input_real_folder = args.inputr
    input_generated_folder = args.inputg
    output_folder = args.output

    os.makedirs(output_folder, exist_ok=True)         
    make_obfuscared_pair(input_real_folder, input_generated_folder, output_folder)