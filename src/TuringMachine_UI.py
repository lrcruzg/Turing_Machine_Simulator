from TuringMachine import TuringMachine
from Tape_UI import Tape_UI
from tkinter import DoubleVar, StringVar


class TuringMachine_UI:
    def __init__(
            self, 
            root, 
            canvas, 
            machine: TuringMachine, 
            cell_size: int, 
            canvas_dimensions: tuple[int, int], 
            state_strvar: StringVar, 
            symbol_strvar: StringVar, 
            steps_strvar: StringVar, 
            speed_var: DoubleVar):
        self.root = root
        self.canvas = canvas
        self.cell_size = cell_size
        self.canvas_dimensions = canvas_dimensions

        self.machine = machine

        self.tape_ui = Tape_UI(
                            self.machine.tape, 
                            canvas, 
                            cell_size, 
                            canvas_dimensions
                        )

        self.state_strvar = state_strvar
        self.symbol_strvar = symbol_strvar
        self.steps_strvar = steps_strvar
        self.speed_var = speed_var

        self.update_strvar()

        self.head = self.create_head()

        self.function_txt = ''
        self.moves_counter = 0
        self.running = False

        self.color_initial_cell()

    def color_initial_cell(self, highlight: bool = True):
        """(Un)Highlight the initial cell. 
        Color the initial cell if highlight, otherwise pait it white
        """
        color = '#e9f6fc' if highlight else "#ffffff"
        self.canvas.itemconfig(
            self.tape_ui.tape_canvas[self.machine.head_position].rect, 
            fill='#e9f6fc'
        )

    def create_head(self):
        canvas_width = self.canvas_dimensions[0]
        canvas_height = self.canvas_dimensions[1]

        head_color = '#1b8ec2'
        
        head_points = [
            canvas_width // 2 + 8, 
            canvas_height // 2 + self.cell_size // 2 + 12, 
            canvas_width // 2, 
            canvas_height // 2 + self.cell_size // 2 + 4,
            canvas_width // 2 - 8, 
            canvas_height // 2 + self.cell_size // 2 + 12,
            canvas_width // 2 - 8, 
            canvas_height // 2 + self.cell_size // 2 + 17,
            canvas_width // 2 + 8, 
            canvas_height // 2 + self.cell_size // 2 + 17
        ]
        
        return self.canvas.create_polygon(*head_points, fill=head_color)

    def update_strvar(self) -> None:
        """Update the UI labels text with the current state of the machine. """
        self.steps_strvar.set(
            f'Steps: {self.machine.steps_counter}'
        )
        
        self.state_strvar.set(
            f'State: {self.machine.current_state}'
        )
        
        self.symbol_strvar.set(
            f'Symbol: {self.machine.tape[self.machine.head_position]}'
        )

    def load_input(self, tape_input: str) -> None:
        """Loads every char of tape_input as a symbol of a Cell on the machine tape. """
        if not len(tape_input):
            return

        self.reset()

        self.color_initial_cell(highlight=False) # un-highlight white the initial cell

        self.machine.load_input(tape_input)

        self.update_strvar()
        self.tape_ui.update_tape()

        self.color_initial_cell(highlight=True) # highlight the initial cell


    def move(self, side) -> None:
        """Move the machine's head to the side given by its argument.
        side = 1, move the head to the left. side = -1, move the head to the  right. """
        if self.moves_counter != self.cell_size // 2:
            self.moves_counter += 1
            self.tape_ui.move(side * 2)
            self.root.after(int(20 * self.speed_var.get()), lambda : self.move(side))
        else:
            self.moves_counter = 0

    def reset(self) -> None:
        """Reset the machine. The tape (head) moves to its initial position, the current
        state is reset to the initial state and the steps counter is reset to 0. """
        self.running = False  # stop the machine if its running

        self.tape_ui.reset()  # reset the tape, set all symbols to B an move to its original position
        self.machine.reset()

        self.update_strvar()

    def load_function(self, file_name) -> None:
        """Loads the transition function from a (txt) file. """
        self.machine.load_function(file_name)
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
        if self.moves_counter != 0:  # can't make a step if there's an animation running
            return 

        if self.machine.step():
            move = self.machine.history[-1][-1]

            self.update_strvar()

            self.tape_ui.update_tape()

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
        if self.machine.current_state != self.machine.final_state and self.running:
            self.step()
            self.root.after(550, self.run)
