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
				
		self.btns_frame = tk.Frame(self.root, relief="ridge", borderwidth=1)
		
		self.state_symb_text = tk.Label(self.btns_frame, 
										textvariable=self.state_symbol_strvar, 
										font=('Helvetica', 12))

		self.steps_text = tk.Label(self.btns_frame, 
								   textvariable=self.steps_strvar, 
								   font=('Helvetica', 12))

		self.step_btn = tk.Button(self.btns_frame, 
								  text='Step',
								  command=self.tm.step)

		self.run_btn = tk.Button(self.btns_frame, 
								 text='Run', 
								 command=self.tm.run_pause)

		self.reset_btn = tk.Button(self.btns_frame, 
								   text='Reset', 
								   command=self.tm.reset)

		self.input_entry = tk.Entry(self.btns_frame,
									textvariable=self.input_strvar)

		self.load_btn = tk.Button(self.btns_frame, 
								  text='Load', 
								  command=lambda : self.tm.load_input(self.input_strvar.get()))

		self.text_frame = tk.Frame(root, relief="ridge", borderwidth=1)

		self.text_box = tk.Text(self.text_frame, 
								state='normal', 
								width=65, 
								height=10)
		
		self.text_box.insert('end', self.tm.function_txt)
		self.text_box['state'] = 'disabled'

		self.canvas.grid(row=0, column=0, columnspan=3)
		self.btns_frame.grid(row=1, column=0, rowspan=4, columnspan=2, sticky='nsew', pady=10, padx=10)
		self.state_symb_text.grid(row=1, column=0, pady=9)
		self.steps_text.grid(row=1, column=1, pady=9)
		self.step_btn.grid(row=2, column=0)
		self.run_btn.grid(row=2, column=1)
		self.reset_btn.grid(row=4, column=0)
		self.input_entry.grid(row=3, column=0, sticky='E')
		self.load_btn.grid(row=3, column=1, sticky='W')
		self.text_frame.grid(row=1 ,column=2, rowspan=4, pady=10, padx=10)
		self.text_box.grid(row=1, column=2, rowspan=4)

		self.root.bind('<s>', lambda event: self.tm.step())
		self.root.bind('<r>', lambda event: self.tm.run_pause())
		self.root.bind('<Escape>', lambda event: self.tm.reset())

	def select_file(self):
		"""Function to select a transition function file (txt). """
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
