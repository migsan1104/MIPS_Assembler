
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
def process_labels(lines, start_text_addr=0x000, start_data_addr=0x000):
    label_table = Label_Table()
    current_text_addr = start_text_addr
    current_data_addr = start_data_addr

    for line in lines:
        section = line.get("section")
        label = line.get("label")

        # assign address
        if section == ".text":
            line["address"] = current_text_addr
            if label:
                label_table.add(label, current_text_addr)
            current_text_addr += 4  # each instruction is one word

        elif section == ".data":
            size = 4  # assume .word for now
            line["address"] = current_data_addr
            if label:
                label_table.add(label, current_data_addr)
            values = line.get("values", [])
            current_data_addr += size * len(values)

    return label_table, lines  # updated lines with addresses
