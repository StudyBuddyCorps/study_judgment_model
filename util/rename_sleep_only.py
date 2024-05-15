import os


def rename_images(folder_path, total_images=10, cycle_length=10):
    image_type = 'study'
    index = 297

    # Get list of image files in the folder
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    image_files = [item for item in image_files if item != ".DS_Store"]
    image_files.sort()
    print(image_files)

    for i, file_name in enumerate(image_files):
        new_name = f"{image_type}_{index}.jpg"
        old_name = os.path.join(folder_path, file_name)
        new_name_with_path = os.path.join(folder_path, new_name)

        try:
            os.rename(old_name, new_name_with_path)
            print(f"Renamed {old_name} to {new_name}")
        except FileNotFoundError:
            print(f"File {old_name} not found.")

        index += 1

# Example usage:
folder_path = "/Users/baejuhyeon/Datasets/capstone/study_dataset/sleep-add/images-rename"
rename_images(folder_path)
