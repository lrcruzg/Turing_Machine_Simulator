from Cell import Cell


class Tape:
    def __init__(self, 
                 num_cells: int, 
                 cell_size: int,
                 center_cell: int,
                 canvas,
                 canvas_width: int,
                 canvas_height: int):
        self.cell_size = cell_size
        self.center_cell = center_cell
        
        self.canvas = canvas
        
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        self.num_cells = num_cells
        self.tape = []
        self.initialize_tape()

    def center_tape(self) -> None:
        """Set the tape position. 
        Places the tape such that the center Cell (i.e. in the center of the canvas) 
        is self.center_cell. 
        """
        initial_position_x = self.canvas_width // 2 - (2 * self.center_cell + 1) * (self.cell_size // 2)
        initial_position_y = self.canvas_height // 2 - self.cell_size // 2
        for i in range(self.num_cells):
            self.tape[i].move_to(initial_position_x + self.cell_size * i, 
                                 initial_position_y)
    
    def initialize_tape(self) -> None:
        """Creates the list of Cells (set the position and default symbol). 
        The default symbol of every cell is 'B'.
        """
        for _ in range(self.num_cells):
            self.tape.append(
                Cell(self.canvas, 0, 0, 
                     self.cell_size, 
                     'B'
                    )
            )

        self.center_tape()  # set position

    def reset(self) -> None:
        """Reset the position and symbol of every cell in the tape. """
        self.center_tape()
        
        for i in range(self.num_cells):
            self[i] = 'B'

    def move(self, side: int) -> None:
        """Move every Cell on the tape to the side given by the argument.
        side = -1 for move to the left, side = 1 for move to the right.
        """
        for i in range(self.num_cells):
            self.tape[i].move(side, 0)

    def __getitem__(self, item):
        """Return the symbol (string). """
        return self.canvas.itemcget(self.tape[item].symbol, 'text')

    def __setitem__(self, key, value):
        """Modifies the symbol text (string). """
        self.canvas.itemconfigure(self.tape[key].symbol, text=value)
