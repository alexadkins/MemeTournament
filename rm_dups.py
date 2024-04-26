import os
import shutil

def remove_duplicate_files(source_dir, target_dir):
    # Get the list of files in the source and target directories
    source_files = set(os.listdir(source_dir))
    target_files = set(os.listdir(target_dir))

    # Find common files and remove them from the source directory
    common_files = source_files.intersection(target_files)

    for common_file in common_files:
        source_file_path = os.path.join(source_dir, common_file)
        os.remove(source_file_path)
        print(f"Removed: {common_file}")

if __name__ == "__main__":
    # Specify your source and target directories
    source_directory = "./remainder_imgs"
    target_directory = "./header_imgs"

    # Call the function to remove duplicate files
    remove_duplicate_files(source_directory, target_directory)
