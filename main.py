from TuringMachine import TuringMachine
import tkinter as tk
from tkinter import filedialog as fd


class App:
	def __init__(self, root):
		self.root = root
		
		self.cell_size = 34
		self.canvas_width = 800
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
		self.state_symbol_strvar = tk.StringVar(value='')

		self.tm = TuringMachine(self.root, 
								self.canvas, 
								self.cell_size, 
								canvas_width=self.canvas_width, 
								canvas_height=self.canvas_height, 
								state_symbol_strvar=self.state_symbol_strvar, 
				 				steps_strvar=self.steps_strvar)

		file_name = './transition_functions/successor_function.txt'
		self.tm.load_function(file_name)
		self.tm.load_input('111')
				
		self.state_text = tk.Label(root, 
								   textvariable=self.state_symbol_strvar
								   )

		self.steps_text = tk.Label(root, 
								   textvariable=self.steps_strvar)

		self.step_btn = tk.Button(root, 
								  text='Step',
								  command=self.tm.step)

		self.run_btn = tk.Button(root, 
								 text='Run', 
								 command=self.tm.run_pause)

		self.reset_btn = tk.Button(root, 
								   text='Reset', 
								   command=self.tm.reset)

		self.input_entry = tk.Entry(root,
									textvariable=self.input_strvar)

		self.load_btn = tk.Button(root, 
								  text='Load', 
								  command=lambda : self.tm.load_input(self.input_strvar.get()))

		self.text_box = tk.Text(self.root, 
								state='normal')
		
		self.text_box.insert('end', self.tm.function_txt)
		self.text_box['state'] = 'disabled'

		self.canvas.grid(row=0, column=0, columnspan=4)
		self.state_text.grid(row=1, column=0)
		self.steps_text.grid(row=1, column=1)
		self.step_btn.grid(row=2, column=0)
		self.run_btn.grid(row=2, column=1)
		self.reset_btn.grid(row=4, column=0)
		self.input_entry.grid(row=3, column=0, sticky='E')
		self.load_btn.grid(row=3, column=1, sticky='W')
		self.text_box.grid(row=1, column=2, columnspan=2, rowspan=4)

	def select_file(self):
		filetypes = (
			('Text files', '*.txt'),
			('All files', '*.*')
		)

		file_name = fd.askopenfilename(
			title='Open the function file.',
			initialdir='./transition_functions/',
			filetypes=filetypes
		)

		if file_name != () and file_name != '':  # a file is selected
			self.tm.reset()
			self.tm.load_function(file_name)
			self.text_box['state'] = 'normal'
			self.text_box.delete('1.0', 'end')
			self.text_box.insert('end', self.tm.function_txt)
			self.text_box['state'] = 'disabled'


def main():
	root = tk.Tk()
	root.title('Turing Machine Simulator')
	app = App(root)
	root.mainloop()

if __name__ == '__main__':
	main()
