import os

def delete_ds_store(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Check for .DS_Store files in the current directory
        ds_store_path = os.path.join(dirpath, '.DS_Store')
        if os.path.isfile(ds_store_path):
            # Delete .DS_Store file
            print(f"Deleting {ds_store_path}")
            os.remove(ds_store_path)

if __name__ == "__main__":
    current_dir = os.getcwd()
    delete_ds_store(current_dir)
