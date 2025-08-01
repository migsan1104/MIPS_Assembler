# MIPS Assembler, turns .asm files into instruction and data .hex files. By default we assume both memory units are 1kb, 1024 bytes = 256 words. 1 word = 4 bytes
import sys
import os
from src.Utilities import write_output_file
from src.Macro_Handler import expand_macros


def main():
    #Error when no input file is given
    if len(sys.argv) < 2:
        print("Usage: python MIPS_Assembler.py <source_file.asm>")
        return

    input_file = sys.argv[1]
    #opening the file and giving an error if it does not exists
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return
    #setting the path of the output files, change them if yours is different
    base = os.path.splitext(os.path.basename(input_file))[0]

    rom_path = f"output/{base}_rom.hex"
    ram_path = f"output/{base}_ram.hex"
    rom_hex = 0
    ram_hex = 0
    write_output_file(rom_path, rom_hex, label="ROM hex")
    write_output_file(ram_path, ram_hex, label="RAM hex")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


