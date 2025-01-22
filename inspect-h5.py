import h5py
import sys

def inspect_h5_file(filepath):
    """
    Inspect the contents of an HDF5 file.
    
    Parameters:
    - filepath: Path to the HDF5 file to inspect.
    """
    try:
        with h5py.File(filepath, 'r') as h5_file:
            print(f"Inspecting HDF5 file: {filepath}")
            print(f"{'-'*40}")
            print(f"File structure:")
            
            def print_structure(name, obj):
                print(f"{name} ({'Group' if isinstance(obj, h5py.Group) else 'Dataset'})")
                if isinstance(obj, h5py.Dataset):
                    print(f"  Shape: {obj.shape}")
                    print(f"  Data type: {obj.dtype}")
                if obj.attrs:
                    print(f"  Attributes: {dict(obj.attrs)}")
            
            h5_file.visititems(print_structure)
            
            print(f"{'-'*40}")
            print("Summary:")
            print(f"  Contains {len(h5_file.keys())} top-level groups/datasets.")
            if h5_file.attrs:
                print(f"  File-level attributes: {dict(h5_file.attrs)}")
    except Exception as e:
        print(f"Error inspecting HDF5 file: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python inspect.py <path_to_h5_file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    inspect_h5_file(filepath)
