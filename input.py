import os

def save_file(file, filename):
    input_folder = './input'
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
    file_path = os.path.join(input_folder, filename)
    file.save(file_path)
    print(f"File saved to {file_path}")
    return file_path