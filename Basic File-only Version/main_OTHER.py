import base64
import os
import tkinter as tk
from tkinter import filedialog, messagebox


def is_base64(string: str):
    """Check if the string is a valid base64 encoded string"""
    try:
        if len(string) % 4 == 0:
            base64.b64decode(string)
            return True
        else:
            return False
    except Exception:
        return False


def save_file(content, original_filename, extension, directory):
    """Saves the content to a file with the original filename plus a suffix"""
    # Get the base filename and original extension
    base_filename, file_extension = os.path.splitext(original_filename)
    
    # Remove '.encoded' from the base filename and extension if present
    if '.encoded' in base_filename:
        base_filename = base_filename.replace('.encoded', '')
    if '.encoded' in file_extension:
        file_extension = file_extension.replace('.encoded', '')
    
    # If decoding, remove the ".encoded" suffix and add ".decoded"
    if extension == ".decoded" and base_filename.endswith(".encoded"):
        base_filename = base_filename[:-8]  # Remove the ".encoded" part
    
    # Construct the new filename with suffix before the extension
    output_filename = f"{base_filename}{file_extension}{extension}"
    output_path = os.path.join(directory, output_filename)
    
    with open(output_path, 'wb') as output_file:
        output_file.write(content)
    return output_path


def browse_file():
    """Opens a file dialog for selecting a file"""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    return filedialog.askopenfilename(title="Select a file")


def main():
    # Step 1: Ask the user to select a file
    file_path = browse_file()

    if not file_path:  # If Cancel is pressed, terminate the script
        print("No file selected. Exiting the script.")
        return

    # Normalize the file path to handle spaces or special characters
    file_path = os.path.normpath(file_path)
    print(f"Selected file: {file_path}")

    # Check if the file path exists and print more details for debugging
    if not os.path.exists(file_path):
        print(f"Error: The file at {file_path} was not found.")
        messagebox.showerror("Error", f"The file at {file_path} was not found.")
        return
    else:
        print(f"File exists: {file_path}")

    # If a file was selected
    original_filename = os.path.basename(file_path)

    # Step 3: Read the file and check if it's Base64 encoded
    try:
        with open(file_path, "rb") as file:
            file_content = file.read()
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        messagebox.showerror("Error", f"The file at {file_path} was not found.")
        return

    if is_base64(file_content.decode('utf-8', errors='ignore')):
        # Step 4: If it's Base64, decode it
        decoded_content = base64.b64decode(file_content)
        save_file(decoded_content, original_filename, ".decoded", os.getcwd())
        messagebox.showinfo("Success", f"File decoded and saved: {file_path}")
    else:
        # Step 5: If it's not Base64, encode it
        encoded_content = base64.b64encode(file_content)
        save_file(encoded_content, original_filename, ".encoded", os.getcwd())
        messagebox.showinfo("Success", f"File encoded and saved: {file_path}")


if __name__ == "__main__":
    main()
