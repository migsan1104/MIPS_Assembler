# line parser, parses line by line to return a dictionary
def parse_lines(lines):

    parsed = []
    current_section = None
    line_no = 0

    for raw_line in lines:
        line_no += 1
        line = raw_line.strip()
        # first we skip blanks and comments
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        label = None


        if line == ".data":
            current_section = ".data"
            continue
        elif line == ".text":
            current_section = ".text"
            continue

        # Show error is we are not in a section
        if current_section is None:
            raise ValueError(f"Line {line_no}: Directive or instruction appears before section (.text/.data)")

        # Handle label
        if line.endswith(":"):
            label = line[:-1]
            parsed.append({
                "label": label,
                "section": current_section
            })
            continue

        # ─── Label + rest on same line ───
        if ":" in line:
            label_part, rest = line.split(":", 1)
            label = label_part.strip()
            rest = rest.strip()
            if not rest:
                parsed.append({
                    "label": label,
                    "section": current_section
                })
                continue
            parts = rest.split()

        # Handling assembler directive
        if parts[0].startswith("."):
            directive = parts[0]

            if directive == ".equ":
                if len(parts) != 4 or parts[2] != "=":
                    raise ValueError(f"Line {line_no}: Invalid .equ format (expected: .equ NAME = VALUE)")
                parsed.append({
                    "directive": ".equ",
                    "name": parts[1],
                    "value": parts[3],
                    "section": current_section
                })

            elif directive in [".org", ".space"]:
                if len(parts) != 2:
                    raise ValueError(f"Line {line_no}: {directive} directive expects one argument")
                try:
                    val = int(parts[1], 0)
                    if directive == ".space" and val < 0:
                        raise ValueError
                except ValueError:
                    raise ValueError(f"Line {line_no}: Invalid argument for {directive}")
                if directive == ".space" and current_section != ".data":
                    raise ValueError(f"Line {line_no}: .space must appear in .data section")

                parsed.append({
                    "directive": directive,
                    "value": parts[1],
                    "section": current_section
                })

            elif directive in [".word", ".byte"]:
                values = []
                for v in parts[1:]:
                    try:
                        values.append(int(v, 0))
                    except ValueError:
                        raise ValueError(f"Line {line_no}: Invalid {directive} value '{v}'")
                parsed.append({
                    "label": label,
                    "directive": directive,
                    "values": values,
                    "section": current_section
                })

            else:
                raise ValueError(f"Line {line_no}: Unknown directive {directive}")

        # assume it is an instruction
        else:
            parsed.append({
                "label": label,
                "instruction": line,
                "section": current_section
            })

    return parsed


