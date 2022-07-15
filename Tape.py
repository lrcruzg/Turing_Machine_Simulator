from Cell import Cell


class Tape:
	def __init__(self,
				 cell_size: int,
				 canvas,
				 canvas_width: int,
				 canvas_height: int):
		self.cell_size = cell_size
		
		self.canvas = canvas
		
		self.canvas_width = canvas_width
		self.canvas_height = canvas_height

		self.n_cells = 40
		self.tape = []
		self.initialize_tape()

	def initialize_tape(self):
		"""Places the Cells of the tape in the middle (height) of the canvas, 
		the second Cell is in the center of the canvas. 
		The default symbol of every cell is 'B'.
		"""
		initial_position_x = self.canvas_width // 2 - 3 * (self.cell_size // 2)
		initial_position_y = self.canvas_height // 2 - self.cell_size // 2

		for i in range(self.n_cells):
			self.tape.append(
				Cell(self.canvas, 
					 initial_position_x + self.cell_size * i, 
					 initial_position_y, 
					 self.cell_size, 
					 'B'
					)
			)

	def reset(self):
		"""Reset the position and symbol of every cell in the tape. """
		initial_position_x = self.canvas_width // 2 - 3 * (self.cell_size // 2)
		initial_position_y = self.canvas_height // 2 - self.cell_size // 2
		for i in range(self.n_cells):
			self.tape[i].move_to(initial_position_x + self.cell_size * i, 
								 initial_position_y)
			self[i] = 'B'

	def move(self, side: int):
		"""Move every Cell on the tape to the side given by the argument.
		side = -1 for move to the left, side = 1 for move to the right.
		"""
		for i in range(self.n_cells):
			self.tape[i].move(side, 0)

	def __getitem__(self, item):
		"""Return the symbol (string). """
		return self.canvas.itemcget(self.tape[item].symbol, 'text')

	def __setitem__(self, key, value):
		"""Modifies the symbol text (string). """
		self.canvas.itemconfigure(self.tape[key].symbol, text=value)
