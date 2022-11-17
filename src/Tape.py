from math import log2


class Tape:
    def __init__(
            self, 
            num_cells: int, 
            default: str = 'B'):
        self.default = default
        self.tape = [default] * num_cells

    @property    
    def num_cells(self) -> int:
        """Returns the size of self.tape. """
        return len(self.tape)

    def resize(self, min_new_size: int) -> None:
        """Resizes the tape copying the information.
        Doubles de size of the tape (if necessary) and the 
        data is copied from the middle.
        """
        if min_new_size > self.num_cells:
            n = int(log2(min_new_size)) + 1
            new_tape = [self.default] * (2 ** n)
            start = (2 ** n) // 2 - self.num_cells // 2
            for i in range(start, start + self.num_cells):
                new_tape[i] = self.tape[i - start]

            self.tape = new_tape

    def reset(self) -> None:
        """Resets the data on the tape. 
        Every cell is set to self.default.
        """
        for i in range(self.num_cells):
            self[i] = self.default

    def __getitem__(self, item):
        return self.tape[item]

    def __setitem__(self, key, value):
        self.tape[key] = value
