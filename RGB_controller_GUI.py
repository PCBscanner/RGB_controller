import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
from tkinter import messagebox
import RGB_controller

def create_input_frame(container):
	frame = ttk.Frame(container)
	row_var = 0
	
	#Options menu for connected devices
	#The selected option is not yet acted upon.
	ttk.Label(frame, text='Device:').grid(column=0, row=row_var, sticky=tk.W)
	options = ['Please scan for devices.']
	variable = tk.StringVar(frame)
	options_cb = ttk.Combobox(frame, textvariable=variable)
	options_cb.grid(column=1, row=row_var, columnspan=2, sticky=tk.W)
	options_cb['values'] = options
	options_cb['state'] = 'readonly'
	row_var = row_var+1
	
	#Brightness input
	ttk.Label(frame, text='Brightness (0 - 10):').grid(column=0, row=row_var, sticky=tk.W)
	brightness_entry = ttk.Entry(frame, width=30)
	brightness_entry.insert(0, 10)
	brightness_entry.grid(column=1, row=row_var, sticky=tk.W)
	row_var = row_var+1
	
	#Color input
	ttk.Label(frame, text='Color code (hex value):').grid(column=0, row=row_var, sticky=tk.W)
	color_entry = ttk.Entry(frame, width=30)
	color_entry.insert(0, 'ffffff')
	color_entry.grid(column=1, row=row_var, sticky=tk.W)
	ttk.Button(frame, text='Choose color', command=lambda: select_color(color_entry)).grid(column=2, row=row_var)
	row_var = row_var+1
	
	#Mode input
	selected_mode = tk.StringVar(frame)
	modes = [['Static single color', 1], ['Static multi color', 2],	['Rainbow wave', 3]]
	mode_label = ttk.Label(frame, text='Select the RGB mode:').grid(column=0, row=row_var, sticky=tk.W)
	row_var = row_var+1
	ttk.Radiobutton(frame, text='Static single color', value=1, variable=selected_mode).grid(column=0, row=row_var, sticky=tk.W)
	row_var = row_var+1
	#ttk.Radiobutton(frame, text='Static multi color', value=2, variable=selected_mode).grid(column=0, row=row_var, sticky=tk.W)
	#row_var = row_var+1
	ttk.Radiobutton(frame, text='Rainbow wave', value=3, variable=selected_mode).grid(column=0, row=row_var, sticky=tk.W)
	row_var = row_var+1
	selected_mode.set(1)
	
	#Button to update RGB on the device - aka send commands
	ttk.Button(frame, text='Update RGB', command=lambda: RGB_controller.external_input(brightness_entry.get(), color_entry.get(), int(selected_mode.get()))).grid(row=row_var, column=1)
	
	#Button to scan for connected devices
	ttk.Button(frame, text='Scan for devices', command=lambda: scan_devices_popup(options_cb)).grid(row=row_var, column=0)
	
	for widget in frame.winfo_children():
		widget.grid(padx=5, pady=5)

	return frame

def update_option_menu(option_menu):
	option_menu['menu'].delete(0, "end")

def select_color(color_entry):
	color = askcolor(title="Tkinter color chooser")
	color_entry.delete(0, 'end')
	color_entry.insert(0, color[1][1:])

def scan_devices_popup(options_cb):
	supported_devices_connected = RGB_controller.scan_devices()
	if supported_devices_connected == []:
		messagebox.showerror('Error', 'No supported devices were found.')
	else:
		messagebox.showinfo('Device(s) found', 'One or more supported devices were found.')
		options_cb_new_values = []
		for dev in supported_devices_connected:
			options_cb_new_values.append(dev[0] + ' ' + dev[2])
		options_cb['values'] = options_cb_new_values
		options_cb.current(0)

def create_main_window():
	root = tk.Tk()
	root.title('RGB controller for SteelSeries Apex 3 TKL')
	root.resizable(0, 0)

	root.columnconfigure(0, weight=4)

	input_frame = create_input_frame(root)
	input_frame.grid(column=0, row=0)
	
	root.mainloop()

if __name__ == "__main__":
    create_main_window()
