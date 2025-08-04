import os
import sys
from Encoder import register_map
def write_output_file(path, lines, label=""):
    output_dir = os.path.dirname(path)

    # Trying to create the directory if it exists in the path
    if output_dir:
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            print(f"❌ Could not create output directory '{output_dir}': {e}")
            return

    # Now we try writing to the file
    try:
        with open(path, "w") as f:
            f.writelines(line + "\n" for line in lines)
        print(f"✅ {label} written to: {path}")
    except FileNotFoundError:
        print(f"❌ Output directory not found or invalid for: {path}")
    except Exception as e:
        print(f"❌ Failed to write {label}: {e}")

def get_register_number(reg_name):
    if reg_name in register_map:
        return register_map[reg_name]
    raise ValueError(f"Unknown register name: {reg_name}")