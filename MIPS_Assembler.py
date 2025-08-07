import os
import sys

# MIPS Assembler, turns .asm files into instruction and data .hex files. By default we assume both memory units are 1kb, 1024 bytes = 256 words. 1 word = 4 bytes
from src.Macro_Handler import expand_macros
from src.Constant_Handler import process_constants
from src.Label_Handler import process_labels
from src.Encoder import encode_instruction
from src.Utilities import write_output_file, encode_data_directives
from src.Line_Parser import parse_lines
#Function that outputs the file, 8 bits (one byte) per line
def write_hex_file(path, data_bytes, label):

    hex_lines = [f"{byte:02X}" for byte in data_bytes]
    write_output_file(path, hex_lines, label)
# returns the raw lines from the .asm file
def read_asm_file(file_path):
    try:
        with open(file_path, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

def main():
    #Handles the error that no
    if len(sys.argv) != 2:
        print("Usage: python assembler.py path/to/input.asm")
        sys.exit(1)

    input_path = sys.argv[1]
    base = os.path.splitext(os.path.basename(input_path))[0]
    #Change this if the path is different
    rom_path = f"Output/{base}_rom.hex"
    ram_path = f"Output/{base}_ram.hex"

    # 1. Reading the .asm file
    raw_lines = read_asm_file(input_path)

    # 2.Expand macros
    expanded_lines = expand_macros(raw_lines)

    # 3. Parse the lines into a list of dictionarys
    parsed_lines = parse_lines(expanded_lines)

    # 4. Process constants by generating the constant table and update the parsed line list
    parsed_lines, constant_table = process_constants(parsed_lines)

    # 5. Process labels by generating the label table and update parsed line list
    label_table, parsed_lines = process_labels(parsed_lines)

    # 6. Seperate text and data lines
    text_lines = []
    data_lines = []
    for line in parsed_lines:
        if line.get("section") == ".text" and "mnemonic":
            text_lines.append(line)
        elif line.get("section") == ".data":
            data_lines.append(line)




    # 7. Encode the text data into a list of rom bytes
    rom_bytes = []
    for i, line in enumerate(text_lines):
        mnemonic = line["mnemonic"]
        operands = line.get("operands", "")
        address = line.get("address", i * 4)  # fallback if address is missing

        try:
            word = encode_instruction(mnemonic, operands, label_table, constant_table, address)
        except Exception as e:
            print(f"❌ Error at line {i + 1}: {mnemonic} {operands} — {e}")
            sys.exit(1)

        # Convert the 32-bit word into 4 bytes - big endian - to process into the .hex file
        rom_bytes.extend([
            (word >> 24) & 0xFF,
            (word >> 16) & 0xFF,
            (word >> 8) & 0xFF,
            word & 0xFF
        ])

    # 8. Encode the data into ram bytes to process into the.hex file
    ram_bytes = encode_data_directives(data_lines)

    # 9. Write back the ram and rom .hex files 
    write_hex_file(rom_path, rom_bytes, "ROM")
    write_hex_file(ram_path, ram_bytes, "RAM")



if __name__ == '__main__':
    main()


