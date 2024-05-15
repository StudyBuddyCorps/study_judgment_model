from PIL import Image
from pillow_heif import register_heif_opener

import os

register_heif_opener()

def convert_heic_to_jpg(folder_path):
    # Get list of HEIC files in the folder
    heic_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.heic')]
    print(len(heic_files))
    for heic_file in heic_files:
        heic_path = os.path.join(folder_path, heic_file)
        # Open HEIC image
        image = Image.open(heic_path)

        # Save as JPG
        jpg_path = os.path.splitext(heic_path)[0].split('/')[-1] + ".jpg"
        jpg_path = os.path.join(save_path, jpg_path)
        # image.convert('RGB').save(jpg_path, "JPEG")
        image.save(jpg_path, format("jpeg"))

        print(f"Converted {heic_file} to JPG.")


# Example usage:
folder_path = "/Users/baejuhyeon/Datasets/capstone/study_dataset/sleep-add/images-before"
save_path = "/Users/baejuhyeon/Datasets/capstone/study_dataset/sleep-add/images-after"
convert_heic_to_jpg(folder_path)
