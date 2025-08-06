# Base64 Encoder/Decoder Tool

A Python-based GUI application for encoding and decoding files or directories in Base64 format.  
Built with **Tkinter** for a modern, user-friendly interface.

---

## Features

- **Automatic Detection**  
  Automatically detects whether a file is Base64-encoded and decides whether to encode or decode.

- **File Processing**  
  - Encodes any file to Base64 and appends `.encoded` to the filename.
  - Decodes Base64 files and restores the original filename (removes `.encoded`).

- **Directory Processing**  
  - Zips the entire directory before encoding.
  - Encoded ZIP is saved with `.encoded` extension.

- **Data Safety**  
  - Original files are never overwritten.
  - Error handling for safe operation.
  - Works with any file type.

- **Help Window**  
  - Built-in detailed instructions via a “How It Works” help popup.

---

## Requirements

- **Python**: 3.7 or later
- No external libraries required (uses standard Python libraries).

---

## Installation

1. Clone or download this repository.
2. Ensure Python 3.x is installed on your system.
3. Run the script:

```bash
python base64-tool.py
