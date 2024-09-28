#This program is currently only set up for the SteelSeries Apex 3 TKL keyboard.

import sys
import usb.core
import usb.util
import binascii
import time

supported_devices = [['Vendor', 'Vendor ID', 'Product', 'Product ID', 'bInterfaceNumber', 'bmRequestType', 'bmRequest', 'wValue', 'wIndex']]
supported_devices.append(['SteelSeries', 0x1038, 'Apex 3 TKL', 0x1622, 0x1, 0x21, 0x9, 0x0200, 0x1])

def detach_device_driver(dev, intf):
	#detaching the device driver if it is busy
	if dev.is_kernel_driver_active(intf):
		print("Kernel driver is attached for interface {0}. Attempting to detach...".format(intf))
		try:
			dev.detach_kernel_driver(intf)
			print("Interface {0} has been detatched.".format(intf))
		except usb.core.USBError as e:
			print(e)
			sys.exit("Could not detach kernel driver from interface {0}".format(intf))
	else:
		print("Kernel driver is not attached for interface {0}.".format(intf))

def attach_device_driver(dev, intf):
	#attaching the device driver
	if not dev.is_kernel_driver_active(intf):
		print("Kernel driver is not attached for interface {0}. Attempting to attach...".format(intf))
		try:
			dev.attach_kernel_driver(intf)
			print("Interface {0} has been attached.".format(intf))
		except usb.core.USBError as e:
			print("Could not attach kernel driver to interface {0}.".format(intf))
			sys.exit(e)
	else:
		print("Kernel driver is already attached for interface {0}.".format(intf))			

def find_dev(idVendor, idProduct):
	print("Finding the device...")
	dev = usb.core.find(idVendor=idVendor, idProduct=idProduct)
	#raising an error if the target device is not found
	if dev is None:
		raise ValueError("Device not found.")
	else:
		print("Found device!")
		return dev

def set_static_single_color_SSA3TKL(dev, dev_params, brightness, color):
	print("Setting a single static color...")
	bmRequestType = dev_params[5]
	bmRequest = dev_params[6]
	wValue = dev_params[7]
	wIndex = dev_params[8]
	#inserting the color value into the correct format for the device
	data_color = '21ff' + color + color + color + color + color + color + color + color
	data_color = data_color + '0000000000000000000000000000000000000000000000000000000000000000000000000000'
	#sending the color data to the device
	dev.ctrl_transfer(bmRequestType, bmRequest, wValue, wIndex, binascii.unhexlify(data_color))
	#inserting the brightness value into the correct format for the device
	data_brightness = '23' + str(brightness).zfill(2)
	data_brightness = data_brightness + '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
	#sending the brightness data to the device
	dev.ctrl_transfer(bmRequestType, bmRequest, wValue, wIndex, binascii.unhexlify(data_brightness))
	print("Data has been sent!")

def set_static_multi_color_SSA3TKL(dev, dev_params, brightness, color):
	print("Setting a static color...")
	bmRequestType = dev_params[5]
	bmRequest = dev_params[6]
	wValue = dev_params[7]
	wIndex = dev_params[8]
	#inserting the color value into the correct format for the device
	data_color = '21ff' + color
	data_color = data_color + '0000000000000000000000000000000000000000000000000000000000000000000000000000'
	#sending the color data to the device
	dev.ctrl_transfer(bmRequestType, bmRequest, wValue, wIndex, binascii.unhexlify(data_color))
	#inserting the brightness value into the correct format for the device
	data_brightness = '23' + str(brightness).zfill(2)
	data_brightness = data_brightness + '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
	#sending the brightness data to the device
	dev.ctrl_transfer(bmRequestType, bmRequest, wValue, wIndex, binascii.unhexlify(data_brightness))
	print("Data has been sent!")

def set_rainbow_wave_SSA3TKL(dev, dev_params, brightness):
	print("Setting a rainbow wave...")
	bmRequestType = dev_params[5]
	bmRequest = dev_params[6]
	wValue = dev_params[7]
	wIndex = dev_params[8]
	#inserting the rainbow wave into the correct format for the device
	data_color = '22ff' + '0000' + '0000'
	data_color = data_color + '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
	#sending the color data to the device
	dev.ctrl_transfer(bmRequestType, bmRequest, wValue, wIndex, binascii.unhexlify(data_color))
	data_brightness = '23' + str(brightness).zfill(2)
	data_brightness = data_brightness + '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
	dev.ctrl_transfer(bmRequestType, bmRequest, wValue, wIndex, binascii.unhexlify(data_brightness))
	print("Data has been sent!")

def get_user_input_mode():
	while True:
		try:
			print("The following modes are available:")
			print("1: Single static color.")
			print("2: Multi-zone static colors.")
			print("3: Rainbow wave.")
			mode = int(input("Enter the mode: "))
			if mode in [1,2,3]:
				break
		except ValueError:
			continue
	return mode

def get_user_input_brightness():	
	while True:
		try:
			brightness = int(input("Enter the integer for the backlight brightness from 0 - 10: "))
			if brightness >= 0 and brightness <= 10:
				break
		except ValueError:
			continue
	return brightness

def get_user_input_color():
	while True:
		try:
			color = str(input("Enter the hex value for the backlight color: "))
			if len(color) == 6:
				break
		except ValueError:
			continue
	return color	

def select_device():
	devs = usb.core.find(find_all=True)
	if devs is None:
		raise ValueError("No devices were found.")
	else:
		print("The following connected devices are supported by this software:")
	supported_devices_connected = []
	i = 0
	for cfg in devs:
		for supported_device in supported_devices:
			if (cfg.idVendor == supported_device[1]) and (cfg.idProduct == supported_device[3]):
				i = i + 1
				print(f"{i}: {supported_device[0]} {supported_device[2]}")
				supported_devices_connected.append(supported_device) 
	selectedDevice = int(input("Select which device you wish to control: "))
	dev = find_dev(supported_devices_connected[selectedDevice-1][1], supported_devices_connected[selectedDevice-1][3])
	return dev, supported_devices_connected[selectedDevice-1]
					
def external_input(brightness, color):
	dev = find_dev(0x1038, 0x1622)
	device_params_default = supported_devices[1]
	detach_device_driver(dev, device_params_default[4])
	set_static_single_color_SSA3TKL(dev, device_params_default, brightness, color)
	usb.util.dispose_resources(dev)
	attach_device_driver(dev, device_params_default[4])
	
def main():
	print("Welcome to an RGB controller written in Python!")
	
	dev, dev_params = select_device()

	#Must ensure the device is not attached otherwise an error will be raised (resource busy)
	#Only need to pass bInterfaceNumber, hence not passing the entire list for dev_params
	detach_device_driver(dev, dev_params[4])
	
	mode = get_user_input_mode()
	brightness = get_user_input_brightness()
	
	if mode == 1:
		color = get_user_input_color()
		set_static_single_color_SSA3TKL(dev, dev_params, brightness, color)
	elif mode == 2:
		color = ''
		for i in range(8):
			color = color + get_user_input_color()
		set_static_multi_color_SSA3TKL(dev, dev_params, brightness, color)
	elif mode == 3:
		set_rainbow_wave_SSA3TKL(dev, dev_params, brightness)
			
	#free up the device resource to proceed.
	usb.util.dispose_resources(dev)
	
	#re-attaching the device to allow other programs to control it.
	attach_device_driver(dev,dev_params[4])
	
	sys.exit()
	
if __name__ == "__main__":
	main()
