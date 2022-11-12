from Tape import Tape
from Cell_UI import Cell_UI

class Tape_UI:
    def __init__(
            self, 
            tape: Tape, 
            canvas, 
            cell_size: int, 
            center_cell: int, 
            canvas_dimensions: tuple[int, int]):
        self.tape = tape
        self.cell_size = cell_size
        self.center_cell = center_cell
        
        self.canvas = canvas
        self.canvas_dimensions = canvas_dimensions

        self.tape_canvas = []

        self.init_tape_canvas()

    def center_tape(self) -> None:
        """Set the tape to its initial position. 
        Places the tape such that the center Cell (i.e. in the center of the canvas) 
        is self.center_cell. 
        """
        canvas_width = self.canvas_dimensions[0]
        canvas_height = self.canvas_dimensions[1]
        
        initial_position_x = canvas_width // 2 - (2 * self.center_cell + 1) * (self.cell_size // 2)
        initial_position_y = canvas_height // 2 - self.cell_size // 2
        for i in range(self.tape.num_cells):
            self.tape_canvas[i].move_to(
                initial_position_x + self.cell_size * i, 
                initial_position_y
            )
    
    def init_tape_canvas(self) -> None:
        """Creates the list of Cells (setting the position and default symbol). 
        The default symbol of every cell is 'B'.
        """
        for i in range(self.tape.num_cells):
            self.tape_canvas.append(
                Cell_UI(
                    self.canvas, 
                    (0, 0),
                    self.cell_size, 
                    self.tape[i]
                )
            )

        self.center_tape()  # set to its initial position

    def update_tape(self):
        """Updates the tape_canvas with respect to tape. """
        for i in range(self.tape.num_cells):
            if self[i] != self.tape[i]:
                self[i] = self.tape[i]

    def reset(self) -> None:
        """Reset the position and symbol of every cell in the tape. """
        self.center_tape()
        self.tape.reset()
        self.update_tape()

    def move(self, side: int) -> None:
        """Move every Cell on the tape to the side given by the argument.
        side = -1 for move to the left, side = 1 for move to the right.
        """
        for i in range(self.tape.num_cells):
            self.tape_canvas[i].move(side, 0)

    def __getitem__(self, item):
        """Return the symbol(string) at tape[item]. """
        return self.canvas.itemcget(
            self.tape_canvas[item].symbol_text, 
            'text'
        )

    def __setitem__(self, key, value):
        """Modifies the symbol (text) displayed in the canvas. """
        self.canvas.itemconfigure(
            self.tape_canvas[key].symbol_text, 
            text=value
        )
