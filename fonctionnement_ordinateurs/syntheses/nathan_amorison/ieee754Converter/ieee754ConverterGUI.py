from ieee754Converter import get_ieee754, ieee754
import tkinter as tk


class MyDoubleEntry(tk.Canvas):
	def __init__(self, parent, text = "", **kwargs):
		super(MyDoubleEntry, self).__init__(parent, kwargs)

		self.var = tk.DoubleVar()

		vcmd = (self.register(self.onValidate), "%d", "%s",'%S')

		label = tk.Label(self, text = text)
		self.entry = tk.Entry(self, textvariable = self.var, validate = 'key', validatecommand = vcmd)

		label.grid(row = 0, column = 0)
		self.entry.grid(row = 0, column = 1)

	def onValidate(self, d, s, S):
		if S:
			if S == "-":
				if s == "" or s == "-":
					return True
				elif d == 0 and s == "":
					return True
				else:
					return False
			elif S.isdecimal() or S == "." or S == "-" or S.replace(".","").isdecimal() or S.replace(".","").isdecimal() or S.replace(".","").replace("-","").isdecimal():
				return True
			else:
				return False

		return True

	def get(self):
		return self.var.get()

class MyBinEntry(tk.Canvas):
	def __init__(self, parent, text = "", **kwargs):
		super(MyBinEntry, self).__init__(parent, kwargs)

		self.var = tk.StringVar()

		vcmd = (self.register(self.onValidate), "%d", "%s",'%S')

		label = tk.Label(self, text = text)
		self.entry = tk.Entry(self, width = 100, textvariable = self.var, validate = 'key', validatecommand = vcmd)

		label.grid(row = 0, column = 0)
		self.entry.grid(row = 0, column = 1)

	def onValidate(self, d, s, S):
		def isBin(string):
			for c in string:
				if c!="0" and c!="1":
					return False
			return True

		if S:
			if isBin(S):
				return True
			else:
				return False

		return True

	def get(self):
		return self.var.get()

class ArchiPannelNum(tk.Canvas):
	def __init__(self,parent, **kwargs):
		super(ArchiPannelNum, self).__init__(parent, kwargs)


		self.var = tk.IntVar()
		self.E_var = tk.IntVar()
		self.B_var = tk.IntVar()
		self.M_var = tk.IntVar()


		self.radio1 = tk.Radiobutton(self, variable = self.var, value = 0, command = self.select)
		self.radio2 = tk.Radiobutton(self, variable = self.var, value = 1, command = self.select)

		label_32_64 = tk.Label(self, text="32/64")

		canvas = tk.Canvas(self)
		label_E = tk.Label(canvas, text="E: ")
		label_B = tk.Label(canvas, text="B: ")
		label_M = tk.Label(canvas, text="M: ")

		vcmd = (self.register(self.onValidate),'%S')

		self.E_entry = tk.Entry(canvas, text="E: ", textvariable = self.E_var, validate = 'key', validatecommand = vcmd, state = tk.DISABLED)
		self.B_entry = tk.Entry(canvas, text="B: ", textvariable = self.B_var, validate = 'key', validatecommand = vcmd, state = tk.DISABLED)
		self.M_entry = tk.Entry(canvas, text="M: ", textvariable = self.M_var, validate = 'key', validatecommand = vcmd, state = tk.DISABLED)


		self.create_line(0,int(self["height"])/2,int(self["width"]), int(self["height"])/2)

		self.radio1.grid(row = 0, column = 0)
		self.radio2.grid(row = 1, column = 0, sticky=tk.N)

		label_32_64.grid(row = 0, column = 1, sticky=tk.W)
		canvas.grid(row = 1, column = 1)

		label_E.grid(row = 0, column = 0)
		label_B.grid(row = 1, column = 0)
		label_M.grid(row = 2, column = 0)
		self.E_entry.grid(row = 0, column = 1)
		self.B_entry.grid(row = 1, column = 1)
		self.M_entry.grid(row = 2, column = 1)

	def onValidate(self, S):
		if S:
			if S.isdecimal():
				return True
			else:
				return False

		return True

	def select(self):
		if self.var.get() == 0:
			self.E_entry.config(state = tk.DISABLED)
			self.B_entry.config(state = tk.DISABLED)
			self.M_entry.config(state = tk.DISABLED)

		else: # elif self.var == 1:
			self.E_entry.config(state = tk.NORMAL)
			self.B_entry.config(state = tk.NORMAL)
			self.M_entry.config(state = tk.NORMAL)

	def get_values(self):
		if self.var.get() == 0:
			return (None, None, None)

		else: # elif self.var == 1:
			return (self.E_var.get(), self.B_var.get(), self.M_var.get(),)

class ArchiPannelBin(tk.Canvas):
	def __init__(self,parent, **kwargs):
		super(ArchiPannelBin, self).__init__(parent, kwargs)


		self.var = tk.IntVar()
		self.E_var = tk.IntVar()
		self.B_var = tk.IntVar()
		self.M_var = tk.IntVar()


		self.radio1 = tk.Radiobutton(self, variable = self.var, value = 0, command = self.select)
		self.radio2 = tk.Radiobutton(self, variable = self.var, value = 1, command = self.select)
		self.radio3 = tk.Radiobutton(self, variable = self.var, value = 2, command = self.select)

		label_32 = tk.Label(self, text="32")
		label_64 = tk.Label(self, text="64")

		canvas = tk.Canvas(self)
		label_E = tk.Label(canvas, text="E: ")
		label_B = tk.Label(canvas, text="B: ")
		label_M = tk.Label(canvas, text="M: ")

		vcmd = (self.register(self.onValidate),'%S')

		self.E_entry = tk.Entry(canvas, text="E: ", textvariable = self.E_var, validate = 'key', validatecommand = vcmd, state = tk.DISABLED)
		self.B_entry = tk.Entry(canvas, text="B: ", textvariable = self.B_var, validate = 'key', validatecommand = vcmd, state = tk.DISABLED)
		self.M_entry = tk.Entry(canvas, text="M: ", textvariable = self.M_var, validate = 'key', validatecommand = vcmd, state = tk.DISABLED)


		self.create_line(0,int(self["height"])/2,int(self["width"]), int(self["height"])/2)

		self.radio1.grid(row = 0, column = 0)
		self.radio2.grid(row = 1, column = 0)
		self.radio3.grid(row = 2, column = 0, sticky=tk.N)

		label_32.grid(row = 0, column = 1, sticky=tk.W)
		label_64.grid(row = 1, column = 1, sticky=tk.W)
		canvas.grid(row = 2, column = 1)

		label_E.grid(row = 0, column = 0)
		label_B.grid(row = 1, column = 0)
		label_M.grid(row = 2, column = 0)
		self.E_entry.grid(row = 0, column = 1)
		self.B_entry.grid(row = 1, column = 1)
		self.M_entry.grid(row = 2, column = 1)

	def onValidate(self, S):
		if S:
			if S.isdecimal():
				return True
			else:
				return False

		return True

	def select(self):
		if self.var.get() == 0 or self.var.get() == 1:
			self.E_entry.config(state = tk.DISABLED)
			self.B_entry.config(state = tk.DISABLED)
			self.M_entry.config(state = tk.DISABLED)

		else: # elif self.var == 1:
			self.E_entry.config(state = tk.NORMAL)
			self.B_entry.config(state = tk.NORMAL)
			self.M_entry.config(state = tk.NORMAL)

	def get_values(self):
		if self.var.get() == 0:
			return (32, 0, 0)

		elif self.var.get() == 1:
			return (64, 0, 0)

		else: # elif self.var == 1:
			return (self.E_var.get(), self.B_var.get(), self.M_var.get(),)


class NumToIeee(tk.Canvas):
	def __init__(self, parent, **kwargs):
		super(NumToIeee, self).__init__(parent, kwargs)

		self.input_val = MyDoubleEntry(self, "input: ")
		self.pannel = ArchiPannelNum(self)
		self.output = tk.Text(self, height=10, width=100)
		self.calc = tk.Button(self, text = "Calculate", command = self.calculate_ieee)

		self.input_val.grid(row = 0, column = 0, columnspan = 1, sticky = tk.W)
		self.pannel.grid(row = 1, column = 0, sticky = tk.W)
		self.output.grid(row = 2, column = 0)
		self.calc.grid(row = 2, column = 1, sticky = tk.E+tk.S)

	def calculate_ieee(self):
		input_number = self.input_val.get()
		E,B,M = self.pannel.get_values()
		
		if E and B and M and E != 0 and B != 0 and M != 0:
			value = get_ieee754(input_number, E = E, B = B, M = M)

			self.output.delete("1.0", "end")
			self.output.insert("end", f"output {1+E+M}-bits: {value}\n")
			self.output.insert("end", f"verification: {str(ieee754(value, E = E, B = B, M = M))}\n")

		elif E == 0 and B == 0 and M == 0:
			self.output.delete("1.0", "end")
			self.output.insert("end", "Please enter correct E B M values or select \"32/64bits\" mod.\n")

		else:
			value64 = get_ieee754(input_number)
			value32 = get_ieee754(input_number, bits=32)

			self.output.delete("1.0", "end")
			self.output.insert("end", f"output 64bits: {value64}\n")
			self.output.insert("end", f"verification 64-bits: {str(ieee754(value64))}\n\n")
			self.output.insert("end", f"output 32bits: {value32}\n")
			self.output.insert("end", f"verification 32-bits: {str(ieee754(value32, bits = 32))}\n")

class IeeeToNum(tk.Canvas):
	def __init__(self, parent, **kwargs):
		super(IeeeToNum, self).__init__(parent, kwargs)

		self.input_val = MyBinEntry(self, "input: ")
		self.pannel = ArchiPannelBin(self)
		self.output = tk.Text(self, height=10, width=100)
		self.calc = tk.Button(self, text = "Calculate", command = self.calculate_num)

		self.input_val.grid(row = 0, column = 0, columnspan = 1, sticky = tk.W)
		self.pannel.grid(row = 1, column = 0, sticky = tk.W)
		self.output.grid(row = 2, column = 0)
		self.calc.grid(row = 2, column = 1, sticky = tk.E+tk.S)

	def calculate_num(self):
		input_number = self.input_val.get()
		E,B,M = self.pannel.get_values()
		
		if E != 0 and B != 0 and M != 0:
			value = str(ieee754(input_number, E = E, B = B, M = M))

			self.output.delete("1.0", "end")
			self.output.insert("end", f"output {1+E+M}-bits: {value}\n")
			self.output.insert("end", f"verification: {str(get_ieee754(value, E = E, B = B, M = M))}\n")

		elif E == 0 and B == 0 and M == 0:
			self.output.delete("1.0", "end")
			self.output.insert("end", "Please enter correct E B M values or select \"32/64bits\" mod.\n")

		elif E == 32 and B == 0 and M == 0:
			value32 = ieee754(input_number, bits=32)

			self.output.delete("1.0", "end")
			self.output.insert("end", f"output 32bits: {value32}\n")
			self.output.insert("end", f"verification 32-bits: {str(get_ieee754(value32, bits = 32))}\n")

		elif E == 64 and B == 0 and M == 0:
			value64 = ieee754(input_number)

			self.output.delete("1.0", "end")
			self.output.insert("end", f"output 64bits: {value64}\n")
			self.output.insert("end", f"verification 64-bits: {str(get_ieee754(value64))}\n\n")


def switch(page):
	global current_page
	global page1_selector
	global page2_selector
	global page1
	global page2
	global container

	if page != current_page:
		current_page = page
		if page == 1:
			page2.forget()
			page1.pack()
			page1_selector.config(bg = "white")
			page2_selector.config(bg = "#353e8c")
		else:
			page1.forget()
			page2.pack()
			page2_selector.config(bg = "white")
			page1_selector.config(bg = "#353e8c")


current_page = 1

win = tk.Tk()


canvas = tk.Canvas(win)

page1_selector = tk.Button(canvas, text="num -> ieee754", command = lambda:switch(1), bg = "white")
page2_selector = tk.Button(canvas, text="ieee754 -> num", command = lambda:switch(2), bg = "#353e8c")

container = tk.Canvas()

page1 = NumToIeee(container)
page2 = IeeeToNum(container)

canvas.grid(row = 0, column = 0, sticky = tk.W)
page1_selector.pack(side=tk.LEFT)
page2_selector.pack(side=tk.LEFT)
container.grid(row = 1, column = 0)
page1.pack()

win.mainloop()