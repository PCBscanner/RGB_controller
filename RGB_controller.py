#This program is currently only set up for the SteelSeries Apex 3 TKL keyboard.

import sys
import usb.core
import usb.util
import binascii
import time

supportedDevices = [['Vendor', 'Vendor ID', 'Product', 'Product ID', 'bInterfaceNumber', 'bmRequestType', 'bmRequest', 'wValue', 'wIndex']]
supportedDevices.append(['SteelSeries', 0x1038, 'Apex 3 TKL', 0x1622, 0x1, 0x21, 0x9, 0x0200, 0x1])

#defaults
colour_default = 'ff4500'
brightness_default = 10
deviceParams_default = supportedDevices[1]

def detachDeviceDriver(dev, intf):
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

def attachDeviceDriver(dev, intf):
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

def findDev(idVendor, idProduct):
	print("Finding the device...")
	dev = usb.core.find(idVendor=idVendor, idProduct=idProduct)
	#raising an error if the target device is not found
	if dev is None:
		raise ValueError("Device not found.")
	else:
		print("Found device!")
		return dev

def setStaticSingleColour_SSA3TKL(dev, devParams, brightness, colour):
	print("Setting a single static colour...")
	bmRequestType = devParams[5]
	bmRequest = devParams[6]
	wValue = devParams[7]
	wIndex = devParams[8]
	#inserting the colour value into the correct format for the device
	dataColour = '21ff' + colour + colour + colour + colour + colour + colour + colour + colour
	dataColour = dataColour + '0000000000000000000000000000000000000000000000000000000000000000000000000000'
	#sending the colour data to the device
	dev.ctrl_transfer(bmRequestType, bmRequest, wValue, wIndex, binascii.unhexlify(dataColour))
	#inserting the brightness value into the correct format for the device
	dataBrightness = '23' + str(brightness).zfill(2)
	dataBrightness = dataBrightness + '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
	#sending the brightness data to the device
	dev.ctrl_transfer(bmRequestType, bmRequest, wValue, wIndex, binascii.unhexlify(dataBrightness))
	print("Data has been sent!")

def setStaticMultiColour_SSA3TKL(dev, devParams, brightness, colour):
	print("Setting a static colour...")
	bmRequestType = devParams[5]
	bmRequest = devParams[6]
	wValue = devParams[7]
	wIndex = devParams[8]
	#inserting the colour value into the correct format for the device
	dataColour = '21ff' + colour
	dataColour = dataColour + '0000000000000000000000000000000000000000000000000000000000000000000000000000'
	#sending the colour data to the device
	dev.ctrl_transfer(bmRequestType, bmRequest, wValue, wIndex, binascii.unhexlify(dataColour))
	#inserting the brightness value into the correct format for the device
	dataBrightness = '23' + str(brightness).zfill(2)
	dataBrightness = dataBrightness + '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
	#sending the brightness data to the device
	dev.ctrl_transfer(bmRequestType, bmRequest, wValue, wIndex, binascii.unhexlify(dataBrightness))
	print("Data has been sent!")

def setRainbowWave_SSA3TKL(dev, devParams, brightness):
	print("Setting a rainbow wave...")
	bmRequestType = devParams[5]
	bmRequest = devParams[6]
	wValue = devParams[7]
	wIndex = devParams[8]
	#inserting the rainbow wave into the correct format for the device
	dataColour = '22ff' + '0000' + '0000'
	dataColour = dataColour + '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
	#sending the colour data to the device
	dev.ctrl_transfer(bmRequestType, bmRequest, wValue, wIndex, binascii.unhexlify(dataColour))
	dataBrightness = '23' + str(brightness).zfill(2)
	dataBrightness = dataBrightness + '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
	dev.ctrl_transfer(bmRequestType, bmRequest, wValue, wIndex, binascii.unhexlify(dataBrightness))
	print("Data has been sent!")

def getUserInput_mode():
	while True:
		try:
			print("The following modes are available:")
			print("1: Single static colour.")
			print("2: Multi-zone static colours.")
			print("3: Rainbow wave.")
			mode = int(input("Enter the mode: "))
			if mode in [1,2,3]:
				break
		except ValueError:
			continue
	return mode

def getUserInput_brightness():	
	while True:
		try:
			brightness = int(input("Enter the integer for the backlight brightness from 0 - 10: "))
			if brightness >= 0 and brightness <= 10:
				break
		except ValueError:
			continue
	return brightness

def getUserInput_colour():
	while True:
		try:
			colour = str(input("Enter the hex value for the backlight colour: "))
			if len(colour) == 6:
				break
		except ValueError:
			continue
	return colour	

def selectDevice():
	devs = usb.core.find(find_all=True)
	if devs is None:
		raise ValueError("No devices were found.")
	else:
		print("The following connected devices are supported by this software:")
	supportedDevicesConnected = []
	i = 0
	for cfg in devs:
		for supportedDevice in supportedDevices:
			if (cfg.idVendor == supportedDevice[1]) and (cfg.idProduct == supportedDevice[3]):
				i = i + 1
				print(f"{i}: {supportedDevice[0]} {supportedDevice[2]}")
				supportedDevicesConnected.append(supportedDevice) 
	selectedDevice = int(input("Select which device you wish to control: "))
	time.sleep(1)
	dev = findDev(supportedDevicesConnected[selectedDevice-1][1], supportedDevicesConnected[selectedDevice-1][3])
	return dev, supportedDevicesConnected[selectedDevice-1]
					
def default():
	dev = findDev(0x1038, 0x1622)
	detachDeviceDriver(dev, deviceParams_default[4])
	setStaticSingleColour_SSA3TKL(dev, deviceParams_default, brightness_default, colour_default)
	usb.util.dispose_resources(dev)
	attachDeviceDriver(dev, deviceParams_default[4])
	sys.exit()
	
def main():
	print("Welcome to an RGB controller written in Python!")
	
	dev, devParams = selectDevice()

	#Must ensure the device is not attached otherwise an error will be raised (resource busy)
	#Only need to pass bInterfaceNumber, hence not passing the entire list for devParams
	detachDeviceDriver(dev, devParams[4])
	
	mode = getUserInput_mode()
	brightness = getUserInput_brightness()
	
	if mode == 1:
		colour = getUserInput_colour()
		setStaticSingleColour_SSA3TKL(dev, devParams, brightness, colour)
	elif mode == 2:
		colour = ''
		for i in range(8):
			colour = colour + getUserInput_colour()
		setStaticMultiColour_SSA3TKL(dev, devParams, brightness, colour)
	elif mode == 3:
		setRainbowWave_SSA3TKL(dev, devParams, brightness)
			
	#free up the device resource to proceed.
	usb.util.dispose_resources(dev)
	
	#re-attaching the device to allow other programs to control it.
	attachDeviceDriver(dev,devParams[4])
	
	sys.exit()
	
if __name__ == "__main__":
	main()
