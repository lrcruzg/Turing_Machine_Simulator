from Tape import Tape
import re


class TuringMachine:
    def __init__(self,
                 root,
                 canvas,
                 cell_size: int,
                 canvas_width: int,
                 canvas_height: int,
                 state_strvar, 
                 symbol_strvar, 
                 steps_strvar):
        self.root = root
        self.canvas = canvas
        self.cell_size = cell_size
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        self.num_cells = 60
        self.initial_head_pos = 30

        self.tape = Tape(self.num_cells,
                         self.cell_size, 
                         self.initial_head_pos, # center_cell
                         self.canvas, 
                         self.canvas_width, 
                         self.canvas_height)

        self.head_position = self.initial_head_pos
        self.initial_state = None
        self.final_state = None

        self.current_state = self.initial_state
        self.steps_counter = 0

        self.state_strvar = state_strvar
        self.symbol_strvar = symbol_strvar
        self.steps_strvar = steps_strvar

        self.update_strvar()

        self.head_movement = {'r': 1, 'l': -1, 'd': 0}

        self.function = {}

        self.head = self.create_head()

        self.function_txt = ''
        self.moves_counter = 0
        self.running = False

    def create_head(self):
        head_color = '#1b8ec2'
        head_points = [
            self.canvas_width // 2 + 8, 
            self.canvas_height // 2 + self.cell_size // 2 + 12, 
            self.canvas_width // 2, 
            self.canvas_height // 2 + self.cell_size // 2 + 4,
            self.canvas_width // 2 - 8, 
            self.canvas_height // 2 + self.cell_size // 2 + 12,
            self.canvas_width // 2 - 8, 
            self.canvas_height // 2 + self.cell_size // 2 + 17,
            self.canvas_width // 2 + 8, 
            self.canvas_height // 2 + self.cell_size // 2 + 17
        ]
        return self.canvas.create_polygon(*head_points, fill=head_color)

    def update_strvar(self) -> None:
        """Update the UI labels text with the current state of the machine. """
        self.steps_strvar.set(f'Steps: {self.steps_counter}')
        self.state_strvar.set(
            f'State: {self.current_state}'
        )
        self.symbol_strvar.set(
            f'Symbol: {self.tape[self.head_position]}'
        )

    def load_input(self, tape_input: str) -> None:
        """Loads every char of tape_input as a symbol of a Cell on the machine tape. """
        if not len(tape_input):
            return
        
        self.reset()
        for i in range(len(tape_input)):
            self.tape[self.head_position + i] = tape_input[i]

    def move(self, side) -> None:
        """Move the machine's head to the side given by its argument.
        side = 1, move the head to the left. side = -1, move the head to the  right. """
        if self.moves_counter != self.cell_size // 2:
            self.moves_counter += 1
            self.tape.move(side * 2)
            self.root.after(18, lambda : self.move(side))
        else:
            self.moves_counter = 0

    def reset(self) -> None:
        """Reset the machine. The tape (head) moves to its initial position, the current
        state is reset to the initial state and the steps counter is reset to 0. """
        self.running = False  # stop the machine if its running
        self.tape.reset()  # reset the tape, set all symbols to B an move to it original position

        # reset all the parameters of the machine to it's original values
        self.current_state = self.initial_state
        self.steps_counter = 0
        self.head_position = self.initial_head_pos
        self.update_strvar()

    def load_function(self, file_name) -> None:
        """Loads the transition function from a (txt) file. """
        tokens = []

        with open(file_name) as f:
            lines = [line.rstrip() for line in f]

        # parse the file
        try:
            for n, line in enumerate(lines):
                if not line.startswith('#'):  # if its not a comment
                    line = line.replace('\n', '')
                    if line:
                        if line.startswith('initial_state'):
                            self.initial_state = re.split(r':', line)[1].strip()
                        elif line.startswith('final_state'):
                            self.final_state = re.split(r':', line)[1].strip()
                        else:
                            line_tokens = re.split(r'[,-]', line)
                            line_tokens = [e.strip() for e in line_tokens]
                            if len(line_tokens) != 5:
                                raise Exception
                            tokens.append(line_tokens)
        except Exception:
            print(f'Error during parsing on line {n + 1}.')
            return

        if not self.initial_state or not self.final_state:
            raise Exception('No initial or final state')
            return

        new_function = {}

        try:
            for c_state, c_symbol, new_state, new_symbol, move in tokens:
                new_function[(c_state, c_symbol)] = (new_state, new_symbol, move)
        except ValueError:
            print('ERROR in transition function')
            self.function = {}
            return 

        self.current_state = self.initial_state

        self.function = new_function

        self.generate_func_txt(file_name)

    def generate_func_txt(self, file_name) -> None:
        """Generates the text to be displayed in the UI text box. """
        txt = ''
        with open(file_name, 'r') as f:
            for line in f:
                txt += line

        self.function_txt = txt

    def step(self) -> None:
        """Run one step the Turing Machine. """

        # can't make a step if there's an animation running
        if self.moves_counter != 0:  
            return 

        if self.current_state == self.final_state:
            print('End State')
            return

        try:
            current_symbol = self.tape[self.head_position]
        except IndexError:
            print(f'The head is out of the tape. Head position = {self.head_position}')
            return

        try:
            new_state, new_symbol, move = self.function[(self.current_state, current_symbol)]
        except KeyError:
            print(f'Instruction (state = {repr(self.current_state)}, '
                  f'symbol = {repr(self.tape[self.head_position])}) is not '
                  f'defined in the function')
            return

        self.current_state = new_state
        self.tape[self.head_position] = new_symbol
        self.head_position += self.head_movement[move]
        self.steps_counter += 1

        self.update_strvar()

        if move == 'l':  # move the head to the left
            self.move(1)
        elif move == 'r':  # move the head to the right
            self.move(-1)

    def run_pause(self) -> None:
        """Run or pause the execution of the machine. """
        if not self.running:
            self.running = True
            self.run()
        else:
            self.running = False

    def run(self) -> None:
        """Run the machine until it reaches the final state or it's paused. """
        if self.current_state != self.final_state and self.running:
            self.step()
            self.root.after(550, self.run)
