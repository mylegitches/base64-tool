File Overview & Functionality Comparison:

1. main_OTHER.py - Basic File-Only Version
•  Simple single-file processor with basic file dialog
•  Opens a file dialog to select ONE file only
•  Automatically detects if the selected file is Base64 encoded or not
•  If Base64: decodes it and saves with .decoded extension
•  If not Base64: encodes it and saves with .encoded extension
•  Limitations: Files only, no directory support, no GUI interface

2. main.py - Full GUI with Separate Buttons
•  Complete GUI application with a persistent window
•  Three separate buttons: "Select a File", "Select a Directory", and "Exit"
•  Handles both individual files AND entire directories
•  For directories: automatically zips the directory first, then processes the zip
•  Same Base64 encoding/decoding logic as others
•  Best user experience with clear options and persistent interface

3. main2.py - Sequential File/Directory Selection
•  Hybrid approach - tries file selection first, then directory if cancelled
•  Single dialog that asks for file first, then falls back to directory selection
•  Same functionality as main.py but with sequential selection process
•  Less intuitive user flow compared to main.py

4. main3.py - Identical to main.py
•  Exactly the same as main.py - appears to be a duplicate
•  Same GUI with three buttons and full functionality

Recommendation:

Use main.py (or main3.py since they're identical) because it offers:
•  ✅ Best user experience with clear, separate buttons for files vs directories
•  ✅ Most flexible - handles both files and directories
•  ✅ Professional GUI that stays open for multiple operations
•  ✅ Directory zipping capability for processing entire folders

npm directory

"C:\nodejs\node.exe" https://github.com/google-gemini/gemini-cli

To encode a file:
python base64_encoder_decoder.py encode <input_file> <output_file>

To decode a file:
python base64_encoder_decoder.py decode <input_file> <output_file>

on Ares-PC
download gemini-cli
unzip it
go to cmd in the directory it is unzipped
run 'npm install --offline'