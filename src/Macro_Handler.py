# assembler/macro_handler.py
#First part of our assembler
def expand_macros(lines):
    '''
    Expands macros defined in the assembly code.
    Currently supports simple macros with no arguments.

    Example:
    .macro DEC
        addi $t0, $t0, -1
    .end_macro

    DEC  → expands into the addi line

    :param lines: list of strings from the .asm file
    :return: list of strings with macros expanded
    '''
    macros = {}  # macro_name -> list of body lines
    expanded = []  # final output
    inside_macro = False
    current_macro_name = ""
    current_macro_body = []

    for line in lines:
        stripped = line.strip()

        # Skip blank lines and comments
        if not stripped or stripped.startswith("#"):
            continue

        # Begin macro
        if stripped.startswith(".macro"):
            parts = stripped.split()
            if len(parts) < 2:
                raise ValueError(f"Invalid macro definition: {line}")
            inside_macro = True
            current_macro_name = parts[1]
            current_macro_body = []
            continue

        # End macro
        elif stripped.startswith(".end_macro"):
            if not inside_macro:
                raise ValueError("Unexpected .end_macro")
            macros[current_macro_name] = current_macro_body.copy()
            inside_macro = False
            current_macro_name = ""
            continue

        # Inside macro: save body lines
        elif inside_macro:
            current_macro_body.append(stripped)
            continue

        # Outside macro: check for macro call
        elif stripped in macros:
            expanded.extend(macros[stripped])
            continue

        # Regular instruction
        else:
            expanded.append(stripped)

    return expanded
