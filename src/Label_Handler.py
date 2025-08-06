
# class to hold labels , dict : label -> address
class Label_Table:
    def __init__(self):
        self.table = {}

    def add_label(self, label, address):
        if label in self.table:
            raise ValueError(f"Duplicate label detected: {label}")
        self.table[label] = address

    def get_address(self, label):
        if label not in self.table:
            raise KeyError(f"Label not found: {label}")
        return self.table[label]

    def has_label(self, label):
        return label in self.table

    def dump(self):
        #print table for debugging
        for label, addr in self.table.items():
            print(f"{label}: {hex(addr)}")

    def export(self):
        # returns copy of internal table
        return dict(self.table)
## label processor that seperates data mem from instruction mem. We also add the correct address to the original lines list
def process_labels(lines, start_text_addr=0x00000000, start_data_addr=0x00000000):
    label_table = Label_Table()
    current_text_addr = start_text_addr
    current_data_addr = start_data_addr

    for line in lines:
        section = line.get("section")
        label   = line.get("label")

        # handle .org directives. Note: .org address assignments are word aligned 
        if line.get("directive") == ".org":
            value_str = line.get("value")
            if value_str is None:
                raise ValueError(f".org directive missing value: {line}")

            new_addr = int(value_str, 0) * 4  # convert word → byte address

            if section == ".text":
                current_text_addr = new_addr
            elif section == ".data":
                current_data_addr = new_addr
            else:
                raise ValueError(f".org directive outside of .text/.data: {line}")
            continue  # skip assigning address to .org line

        # ─── Handle .text section ────────────────────────────────
        if section == ".text":
            line["address"] = current_text_addr
            if label:
                label_table.add_label(label, current_text_addr)
            current_text_addr += 4  # each instruction is 1 word = 4 bytes

        # ─── Handle .data section ────────────────────────────────
        elif section == ".data":
            if label:
                label_table.add_label(label, current_data_addr)

            if line.get("directive") == ".word":
                values = line.get("values", [])
                line["address"] = current_data_addr
                current_data_addr += 4 * len(values)

            elif line.get("directive") == ".byte":
                values = line.get("values", [])
                line["address"] = current_data_addr
                current_data_addr += len(values)  # 1 byte per value

    return label_table, lines

