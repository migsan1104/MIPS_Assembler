
from src.Constant_Handler import ConstantTable, process_constants
from src.Label_Handler import Label_Table,process_labels
# instruction map used to encode/decode
instruction_map = {
    'addiu': {'opcode': '0x09', 'funct': None, 'type': 'I-type'},
    'addu':  {'opcode': '0x00', 'funct': '0x21', 'type': 'R-type'},
    'and':   {'opcode': '0x00', 'funct': '0x24', 'type': 'R-type'},
    'andi':  {'opcode': '0x0C', 'funct': None,  'type': 'I-type'},
    'beq':   {'opcode': '0x04', 'funct': None,  'type': 'Branch'},
    'bgez':  {'opcode': '0x01', 'funct': None,  'type': 'Branch'},
    'bgtz':  {'opcode': '0x07', 'funct': None,  'type': 'Branch'},
    'blez':  {'opcode': '0x06', 'funct': None,  'type': 'Branch'},
    'bltz':  {'opcode': '0x01', 'funct': None,  'type': 'Branch'},
    'bne':   {'opcode': '0x05', 'funct': None,  'type': 'Branch'},
    'j':     {'opcode': '0x02', 'funct': None,  'type': 'Jump'},
    'jal':   {'opcode': '0x03', 'funct': None,  'type': 'Jump'},
    'jr':    {'opcode': '0x00', 'funct': '0x08', 'type': 'R-type'},
    'lw':    {'opcode': '0x23', 'funct': None,  'type': 'Memory'},
    'sw':    {'opcode': '0x2B', 'funct': None,  'type': 'Memory'},
    'mfhi':  {'opcode': '0x00', 'funct': '0x10', 'type': 'R-type'},
    'mflo':  {'opcode': '0x00', 'funct': '0x12', 'type': 'R-type'},
    'mult':  {'opcode': '0x00', 'funct': '0x18', 'type': 'R-type'},
    'multu': {'opcode': '0x00', 'funct': '0x19', 'type': 'R-type'},
    'or':    {'opcode': '0x00', 'funct': '0x25', 'type': 'R-type'},
    'ori':   {'opcode': '0x0D', 'funct': None,  'type': 'I-type'},
    'sll':   {'opcode': '0x00', 'funct': '0x00', 'type': 'R-type'},
    'slt':   {'opcode': '0x00', 'funct': '0x2A', 'type': 'R-type'},
    'slti':  {'opcode': '0x0A', 'funct': None,  'type': 'I-type'},
    'sltiu': {'opcode': '0x0B', 'funct': None,  'type': 'I-type'},
    'sltu':  {'opcode': '0x00', 'funct': '0x2B', 'type': 'R-type'},
    'sra':   {'opcode': '0x00', 'funct': '0x03', 'type': 'R-type'},
    'srl':   {'opcode': '0x00', 'funct': '0x02', 'type': 'R-type'},
    'subu':  {'opcode': '0x00', 'funct': '0x23', 'type': 'R-type'},
    'xor':   {'opcode': '0x00', 'funct': '0x26', 'type': 'R-type'},
    'xori':  {'opcode': '0x0E', 'funct': None,  'type': 'I-type'},
}
#register map
register_map = {
    **{f"r{i}": 0x00 + i for i in range(32)},
    "sp": 0x1E,  # register 30
    "ra": 0x1F   # register 31
}

def get_register_number(reg_name):
    if reg_name in register_map:
        return register_map[reg_name]
    raise ValueError(f"Unknown register name: {reg_name}")

# function used to decode a single line that contains an instruction
def encode_instruction(mnemonic, operands, label_table=None, constants={}, current_address=0):
    info = instruction_map.get(mnemonic)
    if not info:
        raise ValueError(f"Unknown instruction: {mnemonic}")

    instr_type = info["type"]

    if instr_type == "R-type":
        return encode_r_type(mnemonic, operands, info)
    elif instr_type == "I-type":
        return encode_i_type(mnemonic, operands, info, constants)
    elif instr_type == "Branch":
        return encode_branch(mnemonic, operands, info, label_table, current_address, constants)
    elif instr_type == "Jump":
        return encode_jump(mnemonic, operands, info, label_table, constants)
    elif instr_type == "Memory":
        return encode_memory(mnemonic, operands, info, constants, label_table)
    else:
        raise ValueError(f"Unsupported instruction type: {instr_type}")
# encodes r type instructions
def encode_r_type(mnemonic, operands, info):
    opcode = 0
    funct = int(info["funct"], 16)
 # instruction that does not have the typical fields of a r instructions
    if mnemonic in ["sll", "srl", "sra"]:
        # sll rd, rt, shamt
        try:
            rd_str, rt_str, shamt_str = [x.strip() for x in operands.split(",")]
            rd = get_register_number(rd_str)
            rt = get_register_number(rt_str)
            shamt = int(shamt_str, 0)
            rs = 0
        except Exception as e:
            raise ValueError(f"Error parsing shift instruction '{mnemonic}': {e}")
# instruction that does not have the typical fields of a r instruction
    elif mnemonic == "jr":
        # jr rs
        try:
            rs_str = operands.strip()
            rs = get_register_number(rs_str)
            rt = 0
            rd = 0
            shamt = 0
        except Exception as e:
            raise ValueError(f"Error parsing jr: {e}")

    elif mnemonic in ["mfhi", "mflo"]:
        # mfhi rd / mflo rd
        try:
            rd_str = operands.strip()
            rd = get_register_number(rd_str)
            rs = 0
            rt = 0
            shamt = 0
        except Exception as e:
            raise ValueError(f"Error parsing {mnemonic}: {e}")

    else:
        # Standard format: add rd, rs, rt
        try:
            rd_str, rs_str, rt_str = [x.strip() for x in operands.split(",")]
            rd = get_register_number(rd_str)
            rs = get_register_number(rs_str)
            rt = get_register_number(rt_str)
            shamt = 0
        except Exception as e:
            raise ValueError(f"Error parsing standard R-type '{mnemonic}': {e}")

    encoded = (
        (opcode << 26) |
        (rs << 21) |
        (rt << 16) |
        (rd << 11) |
        (shamt << 6) |
        funct
    )

    return encoded
#encodes i type instructions, incorporates the constants table
def encode_i_type(mnemonic, operands, info, constants={}):
    rt_str, rs_str, imm_str = [x.strip() for x in operands.split(",")]
    rt = get_register_number(rt_str)
    rs = get_register_number(rs_str)

    # Checking if the imm is in the constants table
    if imm_str in constants:
        imm = constants[imm_str]
    else:
        imm = int(imm_str, 0)

    imm = imm & 0xFFFF
    # int supports hex,decimal and binary inputs/
    opcode = int(info["opcode"], 16)

    return (
        (opcode << 26) |
        (rs << 21) |
        (rt << 16) |
        imm
    )
# function that eoncodes branch instructions, the target is word aligned
def encode_branch(mnemonic, operands, info, label_table, current_address, constants={}):
    parts = [x.strip() for x in operands.split(",")]

    if mnemonic in ["beq", "bne"]:
        rs = get_register_number(parts[0])
        rt = get_register_number(parts[1])
        target_str = parts[2]
    elif mnemonic in ["bgez", "bltz"]:
        rs = get_register_number(parts[0])
        rt = 1 if mnemonic == "bgez" else 0
        target_str = parts[1]
    elif mnemonic in ["bgtz", "blez"]:
        rs = get_register_number(parts[0])
        rt = 0
        target_str = parts[1]
    else:
        raise ValueError(f"Unsupported branch mnemonic: {mnemonic}")

    # Determine the full byte address of the target
    if target_str in label_table.table:
        target_address = label_table.get(target_str)  # already a byte address
    elif target_str in constants:
        # Assume constants are word-aligned
        target_address = constants[target_str] * 4
    else:
        # Raw numeric offset → treat as word-aligned address
        target_address = int(target_str, 0) * 4

    # Compute the offset relative to PC, turn the byte address into a word address aswell
    offset = (target_address - (current_address + 4)) // 4


    opcode = int(info["opcode"], 16)

    return (
        (opcode << 26) |
        (rs << 21) |
        (rt << 16) |
        (offset & 0xFFFF)
    )

#jump encoder, jump target is word aligned
def encode_jump(mnemonic, operands, info, label_table,constants):
    opcode = int(info["opcode"], 16)
    operand = operands.strip()

    operand = operands.strip()
    # shift addresses in label table due to the fact they are byte aligned
    if label_table and operand in label_table.table:
        target_address = label_table[operand]
        target = target_address >> 2
    elif operand in constants:
        # assume that the constant is already word aligned
        target = constants[operand]
    else:
        target = int(operand, 0)

    target &= 0x03FFFFFF
    return (opcode << 26) | target

# this function encodes mem instructions, although labels are byte addresses, the raw offset fields need to be inputed as word addresses
def encode_memory(mnemonic, operands, info, constants={}, label_table=None):
    try:
        rt_str, mem_expr = [x.strip() for x in operands.split(",")]
        offset_str, rs_str = mem_expr.replace(")", "").split("(")
        rt = get_register_number(rt_str)
        rs = get_register_number(rs_str.strip())
        offset_str = offset_str.strip()

        # Compute byte offset
        if label_table and offset_str in label_table.table:
            offset = label_table.get(offset_str)  # already a byte address
        elif offset_str in constants:
            offset = constants[offset_str] * 4    # word-aligned constant
        else:
            offset = int(offset_str, 0) * 4       # word-aligned

        offset &= 0xFFFF  # wrap to 16-bit
    except Exception as e:
        raise ValueError(f"Failed to parse memory operands: '{operands}'") from e

    opcode = int(info["opcode"], 16)

    return (
        (opcode << 26) |
        (rs << 21) |
        (rt << 16) |
        offset
    )
