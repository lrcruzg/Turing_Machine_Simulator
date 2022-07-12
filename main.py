from TuringMachine import TuringMachine
import tkinter as tk


class App:
	def __init__(self, root):
		self.root = root
		self.canvas_width = 800
		self.canvas_height = 100
		self.canvas = tk.Canvas(self.root, 
								width=self.canvas_width, 
								height=self.canvas_height)
		self.canvas.configure(bg='white')

		self.canvas.grid(row=0, column=0, columnspan=3)

		self.cell_size = 34

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

		file_name = 'succesor_function.txt'
		self.tm.load_function(file_name)
		self.tm.load_input('111')
				
		self.state_text = tk.Label(root, 
								   textvariable=self.state_symbol_strvar
								   ).grid(row=1, column=0)

		self.steps_text = tk.Label(root, 
								   textvariable=self.steps_strvar
								   ).grid(row=1, column=2)

		self.step_btn = tk.Button(root, 
								  text='Step',
								  command=self.tm.step
								  ).grid(row=2, column=1)

		self.run_btn = tk.Button(root, 
								 text='Run', 
								 command=self.tm.run_pause
								).grid(row=2, column=2)

		self.reset_btn = tk.Button(root, 
								   text='Reset', 
								   command=self.tm.reset
								   ).grid(row=2, column=0)

		self.input_entry = tk.Entry(root,
									textvariable=self.input_strvar
									).grid(row=3, column=0, sticky=('E'))

		self.load_btn = tk.Button(root, 
								  text='Load', 
								  command=lambda : self.tm.load_input(self.input_strvar.get())
								  ).grid(row=3, column=1, sticky=('W'))

		self.text_box = tk.Text(self.root, 
								state='normal')
		
		self.text_box.grid(row=4, column=0, columnspan=3)
		
		self.text_box.insert('end', self.tm.function_txt)


def main():
	root = tk.Tk()
	root.title('Turing Machine Simulator')
	app = App(root)
	root.mainloop()

if __name__ == '__main__':
	main()
