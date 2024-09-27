## Introduction
This is a program written in Python to control the RGB lighting of devices.
[PyUSB](https://github.com/pyusb/pyusb) was chosen to send serial commands to the devices.
The motivation was for me to understand more about how USB communication works, and involved reverse engineering the propietary software using a USB packet capturing program.

## Supported devices
* SteelSeries Apex 3 TKL.

## Supported Platforms
This program has only been tested using vanilla Fedora 40.

## Usage
The program can be called simply by entering the following command into a Terminal window:
```
$ python RGB_controller.py
```
This will scan and list the supported devices that are connected to your system.
Selecting the device then brings up the modes supported, such a single static colour, multi-zone static colours, and a rainbow wave.
Brightness and colours are then specified.

A default mode has been added as a separate function, and allows it to be run using a keyboard shortcut without user prompts. This was included because - on my system anyway - the SteelSeries Apex 3 TKL resets to the rainbow wave when waking the computer. An appropriate shortcut to run the default could be:
```
$ cd /path/to/script; python -c 'import RGB_controller; RGB_controller.default()'
```
