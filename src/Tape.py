
class Tape:
    def __init__(
            self, 
            num_cells: int, 
            default: str = 'B'):
        self.default = default
        self.tape = [default] * num_cells

    @property    
    def num_cells(self):
        return len(self.tape)

    def reset(self):
        for i in range(self.num_cells):
            self[i] = self.default

    def __getitem__(self, item):
        return self.tape[item]

    def __setitem__(self, key, value):
        self.tape[key] = value
