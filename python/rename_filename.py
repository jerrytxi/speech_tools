# This script renames files in a specified folder by either removing a suffix or adding a prefix.

import os


def main():
    folder_path = "/Users/cps/Desktop/0-tokenlisation/temp_input_folder/"  # Update this
    num_file = 0

    print("Menu: (1) remove suffix; (2) add prefix")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':  # Remove suffix
        suffix_to_remove = input("Enter the suffix to remove (e.g. _ANLS): ")
        for filename in os.listdir(folder_path):
            name, ext = os.path.splitext(filename)
            if name.endswith(suffix_to_remove):
                new_name = name[:-len(suffix_to_remove)] + ext
                old_path = os.path.join(folder_path, filename)
                new_path = os.path.join(folder_path, new_name)
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} → {new_name}")
                num_file += 1
        print(f"Total files renamed (removed suffix): {num_file}")


    if choice == '2':  # Add prefix
        prefix_to_add= input("Enter the prefix to add (e.g. z-S2T_): ")
        for filename in os.listdir(folder_path):
            old_path = os.path.join(folder_path, filename)
            
            # Skip directories
            if os.path.isfile(old_path):
                new_filename = prefix_to_add + filename
                new_path = os.path.join(folder_path, new_filename)
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} → {new_filename}")
                num_file += 1
        print(f"Total files renamed (added prefix): {num_file}")



if __name__ == '__main__':
    main()