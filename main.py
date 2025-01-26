import os
import sys
import zipfile
import tarfile
import subprocess
from pathlib import Path

def extract_zip(zip_file, output_dir):
    """
    Extracts a zip file into the specified output directory.
    """
    print(f"Extracting {zip_file}...")
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
    print(f"Extracted {zip_file} into {output_dir}.")

def extract_tar_files(input_dir):
    """
    Extracts all .tar files in the given directory into the same directory.
    """
    tar_files = list(Path(input_dir).glob("*.tar"))
    for tar_file in tar_files:
        print(f"Extracting {tar_file}...")
        with tarfile.open(tar_file, 'r') as tar_ref:
            tar_ref.extractall(input_dir)  # Extract contents of .tar into the same directory
        print(f"Extracted {tar_file}.")

def run_events_script(input_dir, events_script_path):
    """
    Runs the events.py script for each .h5 file in the directory.
    """
    h5_files = sorted(Path(input_dir).glob("*.h5"))
    if not h5_files:
        print("No .h5 files found to process.")
        sys.exit(1)

    for h5_file in h5_files:
        timestamp = h5_file.stem.split("_")[1]  # Extract YYYYMMDDHHMM from the filename
        print(f"Processing {h5_file} with events.py...")
        try:
            subprocess.run([sys.executable, events_script_path, timestamp], check=True)
            print(f"Processed {h5_file}.")
        except subprocess.CalledProcessError as e:
            print(f"Error processing {h5_file}: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python process_radar_data.py <zip_file>")
        sys.exit(1)

    # Input zip file
    zip_file = Path(sys.argv[1])
    if not zip_file.exists():
        print(f"Error: File {zip_file} does not exist.")
        sys.exit(1)

    # Define working directory
    output_dir = zip_file.stem  # Use the name of the zip file as the directory name
    output_dir_path = ""

    # Extract the zip file
    extract_zip(zip_file, output_dir_path)

    # Extract all .tar files
    extract_tar_files(output_dir)

    # Path to events.py script
    events_script_path = Path(__file__).parent / "events.py"
    if not events_script_path.exists():
        print(f"Error: events.py not found at {events_script_path}.")
        sys.exit(1)

    # Run events.py for each .h5 file
    run_events_script(output_dir, events_script_path)

if __name__ == "__main__":
    main()
