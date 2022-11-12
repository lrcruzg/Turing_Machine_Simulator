from TuringMachine_UI import TuringMachine_UI
from TuringMachine import TuringMachine
import tkinter as tk
from tkinter import filedialog as fd


class App:
    def __init__(self, root):
        self.root = root

        self.cell_size = 34
        self.canvas_width = 850
        self.canvas_height = 100
        
        self.canvas = tk.Canvas(self.root, 
                                width=self.canvas_width, 
                                height=self.canvas_height)
        self.canvas.configure(bg='white')

        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Open...', 
                                  command=self.select_file)

        self.menubar.add_cascade(label='File', menu=self.filemenu)
        self.root.config(menu=self.menubar)

        self.input_strvar = tk.StringVar(value='')
        self.steps_strvar = tk.StringVar(value='')
        self.state_strvar = tk.StringVar(value='')
        self.symbol_strvar = tk.StringVar(value='')

        self.tm = TuringMachine()

        self.tm_ui = TuringMachine_UI(
                        self.root, 
                        self.canvas, 
                        self.tm, 
                        self.cell_size, 
                        (self.canvas_width, self.canvas_height), 
                        state_strvar=self.state_strvar,
                        symbol_strvar=self.symbol_strvar, 
                        steps_strvar=self.steps_strvar)

        self.file_name = tk.StringVar(value='../transition_functions/successor_function.txt')
        self.tm_ui.load_function(self.file_name.get())
        self.tm_ui.load_input('111')
                
        self.btns_frame = tk.Frame(self.root, 
                                   relief='ridge', 
                                   borderwidth=1)

        self.file_name_label = tk.Label(self.root, 
                                        textvariable=self.file_name, 
                                        font=('Helvetica', 10))

        self.state_label = tk.Label(self.btns_frame, 
                                    textvariable=self.state_strvar, 
                                    font=('Helvetica', 12, 'bold'), 
                                    width=17, 
                                    height=2)

        self.symbol_label = tk.Label(self.btns_frame, 
                                     textvariable=self.symbol_strvar, 
                                     font=('Helvetica', 12, 'bold'), 
                                     width=17, 
                                     height=2)

        self.steps_label = tk.Label(self.root, 
                                    textvariable=self.steps_strvar, 
                                    font=('Helvetica', 10))

        self.step_btn = tk.Button(self.btns_frame, 
                                  text='Step',
                                  command=self.tm_ui.step)

        self.run_btn = tk.Button(self.btns_frame, 
                                 text='Run', 
                                 command=self.tm_ui.run_pause)

        self.reset_btn = tk.Button(self.btns_frame, 
                                   text='Reset', 
                                   command=self.tm_ui.reset)

        self.input_entry = tk.Entry(self.btns_frame,
                                    textvariable=self.input_strvar,
                                    width=15,
                                    borderwidth=4, 
                                    relief=tk.FLAT)

        self.load_btn = tk.Button(self.btns_frame, 
                                  text='Load', 
                                  command=lambda : self.tm_ui.load_input(self.input_strvar.get()))

        self.text_box = tk.Text(self.root, 
                                state='normal',
                                width=60, 
                                height=12)

        self.text_box.insert('end', self.tm_ui.function_txt)
        self.text_box['state'] = 'disabled'

        self.file_name_label.grid(row=0, column=3, sticky='e', padx=10)
        self.steps_label.grid(row=0, column=0, pady=2)

        self.canvas.grid(row=1, column=0, columnspan=4)

        self.btns_frame.grid(row=2, column=0, rowspan=4, columnspan=2, sticky='nsew', pady=10, padx=10)
        self.state_label.grid(row=2, column=0, padx=5, sticky='w')
        self.symbol_label.grid(row=2, column=1, padx=5, sticky='w')

        self.text_box.grid(row=2, column=2, rowspan=4, columnspan=2, padx=10, pady=10)

        self.step_btn.grid(row=3, column=0, pady=9)
        self.run_btn.grid(row=3, column=1, pady=9)

        self.input_entry.grid(row=4, column=0, sticky='e', padx=5)
        self.load_btn.grid(row=4, column=1, sticky='w', pady=20)

        self.reset_btn.grid(row=5, columnspan=2)

        self.root.bind('<s>', lambda event: self.tm_ui.step())
        self.root.bind('<r>', lambda event: self.tm_ui.run_pause())
        self.root.bind('<Escape>', lambda event: self.tm_ui.reset())

    def select_file(self):
        """Function to select a transition function file (txt). """
        filetypes = (
            ('Text files', '*.txt'),
            ('All files', '*.*')
        )

        new_file_name = fd.askopenfilename(
            title='Open the function file.',
            initialdir='../transition_functions/',
            filetypes=filetypes
        )

        if new_file_name != () and new_file_name != '':  # a file is selected
            self.tm_ui.reset()
            self.tm_ui.load_function(new_file_name)
            self.text_box['state'] = 'normal'
            self.text_box.delete('1.0', 'end')
            self.text_box.insert('end', self.tm_ui.function_txt)
            self.text_box['state'] = 'disabled'
            self.file_name.set(new_file_name.split('/')[-1]) # display only the file name


def main():
    root = tk.Tk()
    root.title('Turing Machine Simulator')
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()
