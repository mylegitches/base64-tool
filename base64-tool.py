import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import base64
import os
import subprocess
import sys
import zipfile
import tempfile

def is_base64_encoded(data):
    """Check if data is base64 encoded"""
    try:
        # Try to decode the data
        decoded = base64.b64decode(data, validate=True)
        # Try to re-encode it to verify
        encoded = base64.b64encode(decoded)
        return encoded == data.encode() if isinstance(data, str) else encoded == data
    except Exception:
        return False

def encode_file_to_base64(file_path):
    """Encode a file to base64"""
    with open(file_path, 'rb') as file:
        file_data = file.read()
        encoded_data = base64.b64encode(file_data)
        return encoded_data

def decode_base64_to_file(encoded_data, output_path):
    """Decode base64 data to a file"""
    decoded_data = base64.b64decode(encoded_data)
    with open(output_path, 'wb') as file:
        file.write(decoded_data)

def zip_directory(directory_path):
    """Create a zip archive of a directory"""
    # Create a temporary zip file
    temp_zip = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
    temp_zip.close()
    
    with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, directory_path)
                zipf.write(file_path, arc_path)
    
    return temp_zip.name

def process_file(file_path):
    """Process a single file"""
    try:
        # Read the file content
        with open(file_path, 'rb') as file:
            content = file.read()
        
        # Check if it's already base64 encoded
        if is_base64_encoded(content):
            # Decode and save
            decoded_content = base64.b64decode(content)
            output_path = file_path.replace('.encoded', '')  # Remove .encoded extension
            with open(output_path, 'wb') as file:
                file.write(decoded_content)
            messagebox.showinfo("Success", f"File decoded successfully!\nSaved to: {output_path}")
        else:
            # Encode and save with .encoded extension
            encoded_content = base64.b64encode(content)
            output_path = file_path + '.encoded'
            with open(output_path, 'wb') as file:
                file.write(encoded_content)
            messagebox.showinfo("Success", f"File encoded successfully!\nSaved to: {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def process_directory(directory_path):
    """Process a directory"""
    try:
        # Zip the directory
        zip_path = zip_directory(directory_path)
        
        # Read and encode the zip file
        with open(zip_path, 'rb') as file:
            zip_content = file.read()
            encoded_content = base64.b64encode(zip_content)
        
        # Save the encoded content
        output_path = directory_path + '.encoded'
        with open(output_path, 'wb') as file:
            file.write(encoded_content)
        
        # Clean up temporary zip file
        os.unlink(zip_path)
        
        messagebox.showinfo("Success", f"Directory zipped and encoded successfully!\nSaved to: {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def run_full_service_decoder():
    """Launch the full_service_decoder.py script in a separate process."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, 'full_service_decoder.py')

    if not os.path.exists(script_path):
        messagebox.showerror(
            "Decoder Not Found",
            "Could not locate full_service_decoder.py in the application directory.")
        return

    try:
        subprocess.Popen([sys.executable, script_path], cwd=script_dir)
        messagebox.showinfo(
            "Decoder Started",
            "Full-service decoder is now running in a separate window.\n"
            "Leave this window open until it finishes.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch decoder:\n{e}")
def select_file():
    """Handle file selection"""
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("All files", "*.*")]
    )
    
    if file_path:
        process_file(file_path)

def select_directory():
    """Handle directory selection"""
    directory_path = filedialog.askdirectory(
        title="Select a Directory"
    )
    
    if directory_path:
        process_directory(directory_path)

def show_help_window():
    """Open a separate window with help information"""
    help_window = tk.Toplevel()
    help_window.title("How It Works - Base64 Encoder/Decoder")
    help_window.geometry("600x500")
    help_window.minsize(500, 400)
    
    # Configure colors to match main window
    bg_color = "#f0f0f0"
    text_color = "#333333"
    help_window.configure(bg=bg_color)
    
    # Configure ttk style for help window
    help_style = ttk.Style()
    help_style.configure('Primary.TButton',
                        font=('Segoe UI', 11, 'bold'),
                        padding=(20, 10))
    
    # Make window stay on top initially
    help_window.transient()
    help_window.grab_set()
    
    # Create main frame with padding
    help_frame = ttk.Frame(help_window, padding="20")
    help_frame.pack(fill=tk.BOTH, expand=True)
    
    # Title
    title_label = ttk.Label(help_frame,
                           text="How It Works",
                           font=('Segoe UI', 14, 'bold'))
    title_label.pack(pady=(0, 15))
    
    # Help content in scrollable text widget
    help_text = scrolledtext.ScrolledText(help_frame,
                                         wrap=tk.WORD,
                                         font=('Segoe UI', 10),
                                         bg='white',
                                         fg=text_color,
                                         relief=tk.SUNKEN,
                                         borderwidth=2,
                                         padx=15,
                                         pady=15)
    help_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
    
    help_content = """✅ FILE PROCESSING:

• If the selected file is already Base64 encoded, it will be decoded and saved without the .encoded extension

• If the file is not Base64 encoded, it will be encoded and saved with a .encoded extension

• The tool automatically detects the file format and chooses the appropriate action


✅ DIRECTORY PROCESSING:

• The entire directory is compressed into a ZIP archive first

• The ZIP file is then encoded to Base64 format

• The encoded result is saved with a .encoded extension

• This allows you to bundle multiple files and folders into a single encoded file


✅ OUTPUT FILES:

• Encoded files: original_filename.ext.encoded

• Decoded files: removes the .encoded extension to restore original name

• All operations preserve the original files - nothing is ever overwritten

• You can safely process files without fear of data loss


✅ SUPPORTED FORMATS:

• Any file type can be processed (documents, images, executables, etc.)

• Automatic detection of Base64 encoding

• Safe processing with comprehensive error handling

• No file size limitations (within system memory constraints)


✅ USAGE TIPS:

• Use File Processing for individual files (documents, images, executables, etc.)

• Use Directory Processing to bundle entire folders into a single encoded file

• Encoded files can be safely shared via text-based systems (email, chat, forums, etc.)

• The tool automatically detects whether to encode or decode based on file content

• Original files are never modified - new files are always created

• Base64 encoding increases file size by approximately 33%

• Decoded files should match the original exactly (byte-for-byte)


✅ COMMON USE CASES:

• Sharing binary files through text-only channels

• Embedding files in configuration files or scripts

• Creating portable bundles of multiple files

• Safely transmitting files that might be blocked by email filters

• Converting files for storage in databases or text-based formats"""
    
    help_text.insert(tk.END, help_content)
    help_text.config(state=tk.DISABLED)  # Make it read-only
    
    # Close button
    close_button = ttk.Button(help_frame,
                             text="Close",
                             command=help_window.destroy,
                             style='Primary.TButton')
    close_button.pack(pady=(0, 0))
    
    # Center the window on screen
    help_window.update_idletasks()
    x = (help_window.winfo_screenwidth() // 2) - (help_window.winfo_width() // 2)
    y = (help_window.winfo_screenheight() // 2) - (help_window.winfo_height() // 2)
    help_window.geometry(f"+{x}+{y}")
    
    # Focus on the help window
    help_window.focus_set()

def create_modern_gui():
    """Create a modern, readable GUI interface"""
    root = tk.Tk()
    root.title("Base64 Encoder/Decoder Tool")
    root.geometry("700x450")
    root.resizable(False, False)  # Make window fixed size
    
    # Configure colors and fonts
    bg_color = "#f0f0f0"
    primary_color = "#2196F3"
    secondary_color = "#FFC107"
    text_color = "#333333"
    success_color = "#4CAF50"
    
    root.configure(bg=bg_color)
    
    # Configure ttk style
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure custom styles
    style.configure('Title.TLabel', 
                   font=('Segoe UI', 16, 'bold'),
                   background=bg_color,
                   foreground=text_color)
    
    style.configure('Subtitle.TLabel', 
                   font=('Segoe UI', 10),
                   background=bg_color,
                   foreground='#666666')
    
    style.configure('Primary.TButton',
                   font=('Segoe UI', 11, 'bold'),
                   padding=(20, 10))
    
    style.configure('Secondary.TButton',
                   font=('Segoe UI', 10),
                   padding=(15, 8))
    
    # Create main frame with padding
    main_frame = ttk.Frame(root, padding="30")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Title section
    title_frame = ttk.Frame(main_frame)
    title_frame.pack(fill=tk.X, pady=(0, 20))
    
    title_label = ttk.Label(title_frame, 
                           text="Base64 Encoder/Decoder",
                           style='Title.TLabel')
    title_label.pack()
    
    subtitle_label = ttk.Label(title_frame,
                              text="Encode files and directories to Base64 or decode Base64 back to original format",
                              style='Subtitle.TLabel')
    subtitle_label.pack(pady=(5, 0))
    
    # Separator
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.pack(fill=tk.X, pady=(10, 20))
    
    # Button section
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=tk.X, pady=(0, 30))
    
    # File processing button and description
    file_button = ttk.Button(button_frame,
                            text="📄 Select File to Process",
                            command=select_file,
                            style='Primary.TButton')
    file_button.pack(pady=(0, 5))
    
    file_desc = ttk.Label(button_frame,
                         text="Automatically detects if file is Base64 encoded and converts accordingly",
                         style='Subtitle.TLabel')
    file_desc.pack(pady=(0, 20))
    
    # Directory processing button and description
    directory_button = ttk.Button(button_frame,
                                 text="📁 Select Directory to Process",
                                 command=select_directory,
                                 style='Primary.TButton')
    directory_button.pack(pady=(0, 5))
    
    dir_desc = ttk.Label(button_frame,
                        text="Compresses directory to ZIP format and encodes to Base64",
                        style='Subtitle.TLabel')
    dir_desc.pack(pady=(0, 0))

    decoder_button = ttk.Button(button_frame,
                                text="⚙️ Run Full-Service Decoder",
                                command=run_full_service_decoder,
                                style='Secondary.TButton')
    decoder_button.pack(pady=(25, 5))

    decoder_desc = ttk.Label(
        button_frame,
        text="Launches batch decoder to convert every .encoded file in Downloads",
        style='Subtitle.TLabel')
    decoder_desc.pack()
    
    # Help link section
    help_frame = ttk.Frame(main_frame)
    help_frame.pack(fill=tk.X, pady=(20, 10))
    
    # Add separator line
    help_separator = ttk.Separator(help_frame, orient='horizontal')
    help_separator.pack(fill=tk.X, pady=(0, 10))
    
    # Help link button
    help_link_button = ttk.Button(help_frame,
                                 text="📝 How It Works (Click for detailed help)",
                                 command=show_help_window,
                                 style='Secondary.TButton')
    help_link_button.pack(pady=5)
    
    # Brief help text
    brief_help = ttk.Label(help_frame,
                          text="Need help? Click above to open detailed instructions in a new window",
                          style='Subtitle.TLabel')
    brief_help.pack(pady=(5, 0))
    
    # Status bar
    status_frame = ttk.Frame(root)
    status_frame.pack(fill=tk.X, side=tk.BOTTOM)
    
    status_label = ttk.Label(status_frame, 
                            text="Ready - Select a file or directory to begin",
                            relief=tk.SUNKEN,
                            padding="5")
    status_label.pack(fill=tk.X)
    
    return root

def main():
    """Main application entry point"""
    root = create_modern_gui()
    root.mainloop()

if __name__ == "__main__":
    main()
