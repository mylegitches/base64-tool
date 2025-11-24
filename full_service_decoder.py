import os
import base64
import zipfile

# ==============================
# Configuration (edit as needed)
# ==============================
INPUT_DIRECTORY = r"C:\Users\user\Downloads"
OUTPUT_DIRECTORY = r"C:\Users\user\Downloads\decoded"

# ==============================
# Helper Functions
# ==============================

def is_zip_bytes(data: bytes) -> bool:
    """Return True if the decoded data looks like a ZIP file."""
    # ZIP files start with the bytes 'PK'
    return len(data) >= 2 and data[0:2] == b'PK'


def process_encoded_file(file_path: str):
    """Process a single .encoded file: decode, maybe unzip, and clean up."""
    filename = os.path.basename(file_path)
    name, ext = os.path.splitext(filename)

    # Only touch .encoded files
    if ext.lower() != ".encoded":
        return

    print(f"Processing {filename}...")

    # Read and decode base64
    try:
        with open(file_path, "rb") as f:
            encoded_data = f.read()
        decoded_data = base64.b64decode(encoded_data)
    except Exception as e:
        print(f"ERROR: Failed to base64-decode {filename}: {e}")
        return  # keep the .encoded file for debugging

    # Check if decoded content is a ZIP archive
    if is_zip_bytes(decoded_data):
        # Treat as a zipped archive (directory or file zip)
        zip_name = name + ".zip"
        zip_path = os.path.join(OUTPUT_DIRECTORY, zip_name)
        extract_dir = os.path.join(OUTPUT_DIRECTORY, name)

        print(f"Detected ZIP content. Writing temp zip: {zip_name}")

        try:
            # Write temp zip
            with open(zip_path, "wb") as f:
                f.write(decoded_data)

            # Ensure target extract directory exists
            if not os.path.exists(extract_dir):
                os.makedirs(extract_dir)

            # Extract all
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(extract_dir)

            # Cleanup: remove temp zip and original .encoded
            os.remove(zip_path)
            os.remove(file_path)

            print(f"Extracted to {extract_dir}")
            print(f"Removed temp zip {zip_name} and source {filename}")

        except Exception as e:
            print(f"ERROR: Failed to extract ZIP from {filename}: {e}")
            # On error, keep .encoded and zip (if present) for investigation
            # Don't delete file_path here

    else:
        # Treat as a regular file
        output_path = os.path.join(OUTPUT_DIRECTORY, name)
        try:
            with open(output_path, "wb") as f:
                f.write(decoded_data)

            # Cleanup: remove original .encoded
            os.remove(file_path)

            print(f"Decoded file written to {output_path}")
            print(f"Removed source {filename}")

        except Exception as e:
            print(f"ERROR: Failed to write decoded file for {filename}: {e}")
            # Keep .encoded for debugging


def main():
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    for root, _, files in os.walk(INPUT_DIRECTORY):
        for file in files:
            file_path = os.path.join(root, file)
            process_encoded_file(file_path)


if __name__ == "__main__":
    main()
