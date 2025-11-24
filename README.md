# Base64 Encoder/Decoder Tool

A lightweight desktop utility for Windows that lets you quickly base64-encode individual files or entire folders, decode previously encoded assets, and kick off a bulk decoder for your `Downloads` directory—all from a modern Tkinter UI.

## Features

- **Smart file processing** – automatically detects whether the selected file is raw or already base64 encoded and performs the appropriate action without overwriting the original.
- **Directory support** – compresses a folder to ZIP, base64-encodes it, and saves the archive as `<folder>.encoded`.
- **Batch decoder launcher** – runs `full_service_decoder.py` in a separate process to sweep your Downloads tree for `.encoded` files, decode them, and unzip archives automatically.
- **Detailed help view** – built-in “How it works” window describing typical workflows and safety tips.

## Requirements

- Windows 10 or later
- Python 3.11 (preferred) with Tkinter available

Optional script-specific dependencies (only if you use the historical automation tooling):

- `dev.py` – expects access to `F:\projects\asap`
- `prod.py` – expects an `asap.encoded` file in your Downloads folder and a target path under OneDrive

## Getting Started

```bash
python -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip
python base64-tool.py
```

The GUI launches immediately; use the buttons to process files or directories.

## GUI Workflows

- **Select File to Process** – chooses a single file; the app either encodes it to `<file>.encoded` or decodes it back to the original name.
- **Select Directory to Process** – zips the directory, encodes the ZIP, and saves `<directory>.encoded`.
- **Run Full-Service Decoder** – opens a new console that executes `full_service_decoder.py`. By default that script scans `C:\Users\AXR629\Downloads` (update `INPUT_DIRECTORY` if needed) and writes decoded content to `C:\Users\AXR629\Downloads\decoded`. It detects whether decoded bytes are ZIPs and extracts them automatically.
- **How It Works** – opens reference instructions inside the app.

## Command-Line Utilities

These scripts remain for specialized deployments; they are not required for the GUI.

| Script | Purpose |
| --- | --- |
| `full_service_decoder.py` | Batch-decodes every `.encoded` file under `INPUT_DIRECTORY`, extracting ZIP payloads into `OUTPUT_DIRECTORY`. |
| `dev.py` | Zips `F:\projects\asap`, base64-encodes it, and moves the artifact into `F:\projects\.transfer`. Helpful when preparing artifacts to upload elsewhere. |
| `prod.py` | Reverses the `dev.py` workflow: decodes `asap.encoded` from Downloads, extracts it, and copies the project into `C:\Users\axr629\OneDrive - Aramco Trading Americas\asap\Dev`. |

If you do not use these automation scripts, you can safely ignore or delete them.

## Project Status

Actively maintained in the [`mylegitches/base64-tool`](https://github.com/mylegitches/base64-tool) repository. Contributions and feedback are welcome—open an issue or submit a pull request if you have improvements in mind.

