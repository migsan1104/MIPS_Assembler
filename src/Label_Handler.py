
# class to hold labels , dict : label -> address
class Label_Table:
    def __init__(self):
        self.table = {}

    def __contains__(self, key):
        return key in self.table

    def __getitem__(self, key):
        return self.table[key]


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

    def get(self, name):
        if name not in self.table:
            raise KeyError(f"Constant '{name}' not found")
        return self.table[name]
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

        # Handling text section
        if section == ".text":
            # Always assign current address
            line["address"] = current_text_addr

            if label:
                label_table.add_label(label, current_text_addr)

            # Increment only if it's an instruction
            if "mnemonic" in line:
                current_text_addr += 4
        # Handling data section
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
                padded_count = ((len(values) + 3) // 4) * 4  # we must round like this as demonstrated by the directive handler
                current_data_addr += padded_count

            elif line.get("directive") == ".space":
                line["address"] = current_data_addr
                word_count = int(line["value"], 0)
                current_data_addr += word_count * 4

    return label_table, lines

