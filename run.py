import os
import subprocess
from PIL import Image

SOURCE_FOLDER = "source"
OUTPUT_FOLDER = "output"
TARGET_LONG_EDGE = 2000


def clear_output_folder(folder):
    for f in os.listdir(folder):
        os.remove(os.path.join(folder, f))


def detect_and_replace_extension(file, target_extension="webp"):
    file_name, _ = os.path.splitext(file)
    return f"{file_name}.{target_extension}"


def add_folder_to_path(file, folder):
    return os.path.join(folder, file)


def new_dims(input_path, target_long_edge):
    with Image.open(input_path) as img:
        original_width, original_height = img.size
        is_wide = original_width > original_height
        new_width = (
            target_long_edge
            if is_wide
            else int((target_long_edge / original_height) * original_width)
        )
        new_height = (
            int((target_long_edge / original_width) * original_height)
            if is_wide
            else target_long_edge
        )

        return (new_width, new_height)


def convert_and_optimize(input_path, output_path, w, h):
    command = f"bin/cwebp {input_path} -o {output_path} -resize {w} {h}"
    print(command)
    subprocess.run(command, shell=True)


# Ensure source and output folders exist, create them if they don't
os.makedirs(SOURCE_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Clear the output folder
clear_output_folder(OUTPUT_FOLDER)

input_files = [f for f in os.listdir(SOURCE_FOLDER) if not f.startswith(".")]
output_files = [detect_and_replace_extension(f) for f in input_files]

for input_file, output_file in zip(input_files, output_files):
    input_path = add_folder_to_path(input_file, SOURCE_FOLDER)
    output_path = add_folder_to_path(output_file, OUTPUT_FOLDER)

    w, h = new_dims(input_path, TARGET_LONG_EDGE)

    # Convert and optimize the image
    convert_and_optimize(input_path, output_path, w, h)

print("Image processing completed.")
