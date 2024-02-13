import os

def remove_txt_extension(directory_path):
    # Check if the directory path exists
    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' does not exist.")
        return
    
    # Iterate through files in the directory
    for filename in os.listdir(directory_path):
        # Check if the file ends with ".txt" extension
        if filename.endswith(".txt"):
            # Construct the new file name without the ".txt" extension
            new_filename = os.path.join(directory_path, filename[:-4])
            
            # Rename the file
            os.rename(os.path.join(directory_path, filename), new_filename)
            print(f"Renamed: {filename} -> {new_filename}")

if __name__ == "__main__":
    # Specify the directory path where the files are located
    directory_path = "Algorithm\Algo_1"

    # Call the function to remove ".txt" extension from file names
    paths = os.listdir(directory_path)
    paths.remove(".DS_Store")
    paths.remove("main.py")
    print(paths)
    for path in paths : 
        full_path = os.path.join(directory_path,path)
        if not os.path.isfile(full_path): 
            remove_txt_extension(full_path)
