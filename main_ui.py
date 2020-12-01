import tkinter as tk
import input_manager
import database
import sys
import time
from tkinter import filedialog
import os.path
from tkinter import messagebox
from tkinter import ttk
import playsound as psound

class App:
	def __init__(self, root):
		self.root = root
		self.root.state('zoomed')
		self.root.geometry('1920x1080')
		self.last_change = time.perf_counter()
		self.has_reseted = True
		self.time_until_reset = 2
		self.is_fullscreen = False
		self.widgets()

	def widgets(self):
		self.canvas = tk.Canvas(self.root, background='#999')
		self.canvas.pack(expand=1, fill='both')
		self.root.bind('<Escape>', self.quit)
		self.root.update_idletasks()
		self.text = self.canvas.create_text(self.root.winfo_width() / 2, self.root.winfo_height() / 2, text='please insert cart...', fill='black', font='Arial 24')

		self.top_menu = tk.Menu(self.root)
		self.root.config(menu=self.top_menu)

		self.db_menu = tk.Menu(self.top_menu, tearoff=0)
		self.top_menu.add_cascade(label='database', menu = self.db_menu, underline=0)

		self.db_menu.add_command(label='open from file...', command=self.load_from_file, underline=0)
		self.db_menu.add_command(label='reset...', command=self.reset_db, underline=0)

		self.arduino_menu = tk.Menu(self.top_menu, tearoff=0)
		self.top_menu.add_cascade(label='connect', menu=self.arduino_menu, underline=0)

		self.arduino_menu.add_command(label='change port', command=self.open_change_port)

		self.window_menu = tk.Menu(self.top_menu, tearoff=0)
		self.top_menu.add_cascade(label='window', menu=self.window_menu, underline=0)

		self.window_menu.add_command(label='toogle fullscreen', command=self.toogle_fullscreen, underline=0)

		self.create_db()
		self.load_db()
		self.update()

	def create_db(self):
		if not os.path.isfile(database.file_name):
			file = filedialog.askopenfile()
			database.create_db(database.file_name, database.open_from_file(file.name, _encoding=file.encoding))

	def load_db(self):
		self.students = database.load_db(database.file_name)

	def update(self):
		number = input_manager.read()

		if number == -1:
			messagebox.showerror('Error', 'No arduino connected on Port {}!\nPlease connect an arduino and restart the app.'.format(input_manager.port))
		else:
			if number and number.isdigit():
				print(number)
				number = int(number)
				if not database.check(number, self.students, database.file_name):
					self.canvas['background'] = '#21cf0f'
					self.canvas.itemconfig(self.text, text='Free to pass... Have a nice lunch!')
					psound.playsound('enter_sound.wav')
					psound.playsound('enter_sound.wav')
				else:
					self.canvas['background'] = '#e81f1f'
					self.canvas.itemconfig(self.text, text="Oh... It seems that you've eaten already!") 
					psound.playsound('deny_sound.wav')

				self.last_change = time.perf_counter()
				self.has_reseted = False

			self.canvas.after(10, self.update)
			if time.perf_counter() >= self.last_change + self.time_until_reset and not self.has_reseted:
				self.reset_scene()
				self.has_reseted = True

	def quit(self, event):
		print('exiting application')
		self.root.destroy()

	def reset_scene(self):
		self.canvas['background'] = '#999'
		self.canvas.itemconfig(self.text, text="please insert cart...")
		# print('resetting...')

	def reset_db(self):
		ans = messagebox.askyesno('reset databasse', 'are you sure you want to reset the databse?')
		if ans:
			database.reset_db(database.file_name)
			self.load_db()
			messagebox.showinfo('reset database', 'the database is reset!')

	def load_from_file(self):
		file = filedialog.askopenfile()
		if file != None:
			database.update_db(database.file_name, database.open_from_file(file.name, _encoding=file.encoding))
			self.load_db()
			messagebox.showinfo('open file', 'database sucessfully loaded!')

	def open_change_port(self):
		print(input_manager.list_ports())
		self.port_window = tk.Toplevel()

		self.port_value = tk.StringVar()
		self.ports_menu = ttk.Combobox(self.port_window, textvariable=self.port_value)
		self.ports_menu.bind("<<ComboboxSelected>>", self.change_port)
		selections = []
		for p in input_manager.list_ports():
			selections.append(p)
		self.ports_menu['values'] = selections
		self.ports_menu.pack(side='bottom')
		description_label = tk.Label(self.port_window, text='select avaliable port:', anchor='w', width=20)
		description_label.pack(side='bottom')

	def toogle_fullscreen(self):
		self.is_fullscreen = not self.is_fullscreen
		self.root.attributes('-fullscreen', self.is_fullscreen)

	def change_port(self, e):
		port = self.port_value.get().split(' ')[0]
		print(f'changing port to {port}...')
		input_manager.port = port

w = tk.Tk()
# w.attributes("-fullscreen", True)
app = App(w)
w.mainloop()