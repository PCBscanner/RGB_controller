import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
import RGB_controller

def create_input_frame(container):
	frame = ttk.Frame(container)

	ttk.Label(frame, text='Brightness (0 - 10):').grid(column=0, row=0, sticky=tk.W)
	brightness_entry = ttk.Entry(frame, width=30)
	brightness_entry.insert(0, 10)
	brightness_entry.grid(column=1, row=0, sticky=tk.W)

	ttk.Label(frame, text='Color code (hex value):').grid(column=0, row=1, sticky=tk.W)
	color_entry = ttk.Entry(frame, width=30)
	color_entry.insert(0, 'ffffff')
	color_entry.grid(column=1, row=1, sticky=tk.W)

	ttk.Button(frame, text='Choose color', command=lambda: select_color(color_entry)).grid(column=2, row=1)
	
	ttk.Button(frame, text='Update RGB', command=lambda: RGB_controller.external_input(brightness_entry.get(), color_entry.get())).grid(row=2, columnspan=3)
	
	for widget in frame.winfo_children():
		widget.grid(padx=5, pady=5)

	return frame

def update_RGB(brightness, color):
	print("Updating RGB...")
	print(f"Brightness is: {brightness}")
	print(f"Color is: {color}")

def select_color(color_entry):
	color = askcolor(title="Tkinter color chooser")
	color_entry.delete(0, 'end')
	color_entry.insert(0, color[1][1:])

def create_main_window():
	root = tk.Tk()
	root.title('RGB controller')
	root.resizable(0, 0)

	root.columnconfigure(0, weight=4)

	input_frame = create_input_frame(root)
	input_frame.grid(column=0, row=0)
	
	root.mainloop()

if __name__ == "__main__":
    create_main_window()
