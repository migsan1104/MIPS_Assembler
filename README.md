# MIPS Assembler

This project implements a custom three-pass assembler in Python for a simplified MIPS-like processor. The assembler translates `.asm` files into two hex files: one for ROM (instruction memory) and one for RAM (data memory).

---

## ✅ Features

### Supported Sections
- `.data` section for global data
- `.text` section for instructions

### Supported Directives
- `.word`: stores one or more 32-bit words
- `.byte`: stores bytes (packed into 32-bit words, padded MSB-first)
- `.space`: reserves uninitialized memory in words
- `.org`: sets memory address offset (word-aligned)
- `.equ`: defines constants usable in code and data

### Macro Support
- `.macro` / `.end_macro` block-style macros
- No-argument support (simple inline expansion)
- Macros are expanded in a preprocessing pass before parsing

### Supported Instruction Types
- R-type (e.g., `addu`, `subu`, `jr`)
- I-type (e.g., `addiu`, `lw`, `sw`, `beq`, `bne`, `bgtz`, `blez`, `bltz`, `bgez`)
- J-type (e.g., `j`, `jal`)

### Output
- Two hex files are generated:
  - `*_rom.hex` for instruction memory (byte-addressed)
  - `*_ram.hex` for data memory (byte-addressed, big-endian)

---

## 🧠 How It Works

### Pass 1: Line Parsing and Macro Expansion
- Reads `.asm` line by line
- Expands macros before actual parsing
- Tracks `.text` and `.data` section boundaries
- Builds an intermediate list of parsed line dictionaries

### Pass 2: Label and Constant Resolution
- All labels are stored in a `LabelTable` during this pass
- Byte addresses are assigned per instruction or directive
- `.org` directives jump memory ahead
- `.space`, `.byte`, and `.word` increment memory pointers
- Constants defined via `.equ` are processed here

### Pass 3: Encoding
- Each instruction is encoded based on its type and operands
- All branch/jump targets are resolved through `LabelTable`
- Constants are substituted into operand fields
- `.word` values are split into big-endian bytes
- `.byte` values are grouped into 32-bit words with padding

---

## 🧱 Internal Components

### LabelTable Class

Used to track all labels and their byte-addresses (for both `.text` and `.data`):

- `add_label(label, address)`
- `get_address(label)`
- `__contains__` and `__getitem__` overloads for convenience

### ConstantTable Class

Handles all `.equ` constants used in both code and data:

- `.equ NAME = VALUE` creates a constant (e.g., `.equ SIZE = 4`)
- Constants are resolved during label processing
- API:
  - `add(name, value)`
  - `get(name)`
  - `__contains__` and `__getitem__`

---

## 🧪 Testing

The assembler has been validated against a set of test `.asm` files, including:
- Instruction encoding
- Branch/jump resolution
- Macro expansion
- Alignment with `.org`, `.space`, `.byte`, and `.word`

Tests confirm accurate ROM and RAM output as used on a custom MIPS-like pipelined processor implemented in SystemVerilog.

---

## 🛠 How to Build Your Own Assembler

1. **Preprocess Macros**  
   Scan the raw lines for `.macro` / `.end_macro` blocks and expand them inline.

2. **Parse Cleaned Lines**  
   Strip comments, handle labels and directives, and produce an intermediate dictionary format for each line.

3. **Build Label and Constant Tables**  
   Walk through parsed lines to assign addresses to labels and evaluate `.equ` constants. Apply `.org`, `.space`, `.word`, and `.byte` alignment rules.

4. **Encode Instructions and Data**  
   Use the resolved label and constant addresses to encode:
   - Instructions into 32-bit machine code
   - Data into memory-aligned byte lists

5. **Output to `.hex`**  
   Write the encoded ROM and RAM contents as byte-per-line hexadecimal files in big-endian format.
