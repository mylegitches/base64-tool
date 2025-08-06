import base64
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import io
 
 
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
 
 
def browse_file_or_directory(is_folder=False):
    """Opens a file dialog for selecting a file or directory based on the argument"""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
 
    if is_folder:
        # Ask the user to select a directory
        selected_path = filedialog.askdirectory(title="Select a directory")
    else:
        # Ask the user to select a file
        selected_path = filedialog.askopenfilename(title="Select a file")
 
    return selected_path
 
 
def zip_directory(directory_path):
    """Zips the selected directory"""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for folder_name, subfolders, filenames in os.walk(directory_path):
            for filename in filenames:
                file_path = os.path.join(folder_name, filename)
                zip_file.write(file_path, os.path.relpath(file_path, directory_path))
    return zip_buffer.getvalue()
 
 
def on_button_click(is_folder=False):
    """Handles the button click for file or directory selection"""
    selected_path = browse_file_or_directory(is_folder)
 
    if not selected_path:  # If Cancel is pressed, terminate the script
        print("No file or directory selected. Exiting the script.")
        return
 
    # Normalize the file path to handle spaces or special characters
    selected_path = os.path.normpath(selected_path)
    print(f"Selected path: {selected_path}")
 
    # Check if the selected path exists and print more details for debugging
    if not os.path.exists(selected_path):
        print(f"Error: The file or directory at {selected_path} was not found.")
        messagebox.showerror("Error", f"The file or directory at {selected_path} was not found.")
        return
    else:
        print(f"Path exists: {selected_path}")
 
    # If a directory was selected, zip it
    if os.path.isdir(selected_path):
        print(f"Zipping directory: {selected_path}")
        file_content = zip_directory(selected_path)
        original_filename = os.path.basename(selected_path) + ".zip"
    else:
        # If a file was selected, read its content
        original_filename = os.path.basename(selected_path)
        try:
            with open(selected_path, "rb") as file:
                file_content = file.read()
        except FileNotFoundError:
            print(f"Error: The file at {selected_path} was not found.")
            messagebox.showerror("Error", f"The file at {selected_path} was not found.")
            return
 
    # Step 3: Check if the content is Base64 encoded
    if is_base64(file_content.decode('utf-8', errors='ignore')):
        # Step 4: If it's Base64, decode it
        decoded_content = base64.b64decode(file_content)
        save_file(decoded_content, original_filename, ".decoded", os.getcwd())
        messagebox.showinfo("Success", f"File decoded and saved: {selected_path}")
    else:
        # Step 5: If it's not Base64, encode it
        encoded_content = base64.b64encode(file_content)
        save_file(encoded_content, original_filename, ".encoded", os.getcwd())
        messagebox.showinfo("Success", f"File encoded and saved: {selected_path}")
 
 
def main():
    """Create a basic tkinter window with 3 buttons"""
    root = tk.Tk()
    root.title("File/Directory Selection")
 
    # Button to select a file
    file_button = tk.Button(root, text="Select a File", command=lambda: on_button_click(is_folder=False))
    file_button.pack(padx=10, pady=10)
 
    # Button to select a directory
    dir_button = tk.Button(root, text="Select a Directory", command=lambda: on_button_click(is_folder=True))
    dir_button.pack(padx=10, pady=10)
 
    # Button to exit the application
    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.pack(padx=10, pady=10)
 
    # Run the Tkinter main loop
    root.mainloop()
 
 
if __name__ == "__main__":
    main()