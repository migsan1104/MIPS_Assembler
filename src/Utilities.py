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
#converts .data section directives into the bytes needed for the data memory hex file
def encode_data_directives(lines):

    byte_list = []
    current_addr = 0
    byte_buffer = []  # holds pending .byte values

    def flush_byte_buffer():
        #using nonlocal variable access
        nonlocal current_addr
        while byte_buffer:
            group = byte_buffer[:4]
            del byte_buffer[:4]
            padding = [0x00] * (4 - len(group))  # pad left (MSBs)
            full_word = padding + group
            byte_list.extend(full_word)
            current_addr += 4

    for line in lines:
        if line.get("section") != ".data":
            continue

        directive = line.get("directive")

        # handling .org
        if directive == ".org":
            flush_byte_buffer()
            new_addr = int(line["value"], 0) * 4  # word-aligned
            padding = new_addr - current_addr
            if padding < 0:
                raise ValueError(f".org address {hex(new_addr)} precedes current address {hex(current_addr)}")
            byte_list.extend([0x00] * padding)
            current_addr = new_addr

        # ─── .byte ───
        elif directive == ".byte":
            for val in line.get("values", []):
                byte_buffer.append(val & 0xFF)

        # ─── .word ───
        elif directive == ".word":
            flush_byte_buffer()
            for val in line.get("values", []):
                word_bytes = [
                    (val >> 24) & 0xFF,
                    (val >> 16) & 0xFF,
                    (val >> 8) & 0xFF,
                    val & 0xFF
                ]
                byte_list.extend(word_bytes)
                current_addr += 4

        # ─── .space ───
        elif directive == ".space":
            flush_byte_buffer()
            word_count = int(line["value"], 0)
            byte_count = word_count * 4
            byte_list.extend([0x00] * byte_count)
            current_addr += byte_count

        # ─── Skip other directives (e.g., .equ) ───
        else:
            continue

    flush_byte_buffer()  # flush any remaining bytes
    return byte_list

