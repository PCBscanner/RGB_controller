# Introduction
This is a program written in Python to control the RGB lighting of devices.
[PyUSB](https://github.com/pyusb/pyusb) was chosen to send serial commands to the devices.
The motivation was for me to understand more about how USB communication works, and involved reverse engineering the propietary software using a USB packet capturing program.

# Supported Devices
* SteelSeries Apex 3 TKL.

# Supported Platforms
This program has only been tested using vanilla Fedora 40.

# Prerequisites
You must have the following installed to run certain parts of the program:
* Controller: [PyUSB](https://github.com/pyusb/pyusb).
* GUI: [Tkinter](https://docs.python.org/3/library/tkinter.html).

# Usage
## GUI (Standard)
The recommended way to run this program is using the GUI:
```
$ python /path/to/script/RGB_controller_GUI.py
```
The GUI currently only supports setting a single static colour.

## Manual Mode
Alternatively, the program can be called by entering the following command into a Terminal window:
```
$ python /path/to/script/RGB_controller.py
```
This comes with additional functionality of setting colours by zone or setting a rainbow wave effect.


This will scan and list the supported devices that are connected to your system.
Selecting the device then brings up the modes supported, such a single static colour, multi-zone static colours, and a rainbow wave.
Brightness and colours are then specified.

## Shortcut Mode
A default mode has been added as a separate function, and allows it to be run using a keyboard shortcut without user prompts. This was included because - on my system anyway - the SteelSeries Apex 3 TKL resets to the rainbow wave when waking the computer. An example shortcut to run this would be:
```
$ cd /path/to/script; python -c 'import RGB_controller; RGB_controller.external_input(10, "ffffff")'
```
