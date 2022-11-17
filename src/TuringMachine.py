import sys
sys.path.append('../')

from src.Tape import Tape
import re


class TuringMachine:
    def __init__(
            self, 
            function: dict = None, 
            initial_state: str = None, 
            final_state: str = None):
        self.function = function
        self.tape = Tape(num_cells=64)

        self.head_position = self.initial_head_position
        self.initial_state = initial_state
        self.final_state = final_state

        self.current_state = self.initial_state
        self.steps_counter = 0

        self.head_movement = {'r': 1, 'l': -1, 'd': 0}

        # (prev. symbol, prev. state, curr. symbol, curr. state)
        self.history = []


    @property
    def num_cells(self) -> int:
        """Return the size of self.tape. """
        return self.tape.num_cells


    @property
    def initial_head_position(self) -> int:
        """Return the size of self.tape. """
        return self.num_cells // 2


    def step(self) -> bool:
        """Runs the machine one step.
        Returns True if the machine could run one step, otherwise returns False.
        """
        if not self.function:
            return False

        if self.current_state == self.final_state:
            return False

        try:
            current_symbol = self.tape[self.head_position]
        except IndexError:
            print(f'Head out of the tape. Head position = {self.head_position}')
            return False

        try:
            new_state, new_symbol, move = self.function[(self.current_state, current_symbol)]
        except KeyError:
            print(
                f'Instruction (state = {repr(self.current_state)}, '
                f'symbol = {repr(self.tape[self.head_position])}) '
                f'is not defined'
            )
            return False

        self.history.append(
            (current_symbol, self.current_state, new_symbol, new_state, move)
        )

        self.current_state = new_state
        self.tape[self.head_position] = new_symbol
        self.head_position += self.head_movement[move]
        self.steps_counter += 1

        return True


    def load_function(self, file_name) -> None:
        """Loads the transition function from a (txt) file. """
        tokens = []

        with open(file_name) as f:
            lines = [line.rstrip() for line in f]

        # Parse the file
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
            print('No initial or final state')
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


    def reset(self):
        """Reset all the parameters of the machine to it's original values. """
        self.tape.reset()  # reset the tape

        self.head_position = self.initial_head_position
        self.current_state = self.initial_state
        self.steps_counter = 0
        self.history = []


    def load_input(self, tape_input: str) -> None:
        """Loads every char of tape_input as a symbol of a Cell on the machine tape. """
        if not len(tape_input):
            return
        
        if self.num_cells // 2 < len(tape_input): # input doesn't fit in the 2nd half
            self.tape.resize(len(tape_input) * 2) # at leas should fit int the 2nd half

        self.reset()

        for i, c in enumerate(tape_input):
            self.tape[self.head_position + i] = c
