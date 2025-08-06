# class to hold constants defined with .EQU (e.g., VALUE = 0x10)
class ConstantTable:
    def __init__(self):
        self.table = {}

    def add(self, name, value):
        if name in self.table:
            raise ValueError(f"Duplicate constant: {name}")
        self.table[name] = value

    def get(self, name):
        if name not in self.table:
            raise KeyError(f"Constant '{name}' not found")
        return self.table[name]

    def has(self, name):
        return name in self.table

    def dump(self):
        for name, value in self.table.items():
            print(f"{name}: {hex(value)}")

    def export(self):
        return dict(self.table)

# function that creates the constant table from the lines
def process_constants(lines):
    const_table = ConstantTable()

    for line in lines:
        if line.get("directive") == ".EQU":
            label = line.get("label")
            value_str = line.get("value")

            if not label or value_str is None:
                raise ValueError(f"Invalid .EQU directive: {line}")

            # Convert value string to int (supports hex, binary, decimal)
            value = int(value_str, 0)
            const_table.add(label, value)

    return const_table
