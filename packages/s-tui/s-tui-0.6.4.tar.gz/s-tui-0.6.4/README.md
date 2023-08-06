# The Stress Terminal UI: s-tui

[![Build Status](https://travis-ci.org/amanusk/s-tui.svg?branch=master)](https://travis-ci.org/amanusk/s-tui)
[![PyPI version](https://badge.fury.io/py/s-tui.svg)](https://badge.fury.io/py/s-tui)


s-tui is a terminal UI for monitoring your computer. s-tui allows to monitor CPU temperature, frequency, power and utilization in a graphical way from the terminal. 

## Screenshot
![](https://github.com/amanusk/s-tui/blob/master/ScreenShots/s-tui.gif?raw=true)

* [The Stress Terminal UI: s-tui](#the-stress-terminal-ui-s-tui)
  * [Screenshot](#screenshot)
  * [What it does](#what-it-does)
  * [Usage](#usage)
  * [Simple installation](#simple-installation)
	 * [pip (x86   ARM)](#pip-x86--arm)
	 * [Run local executable (x86 only):](#run-local-executable-x86-only)
  * [Options](#options)
  * [Dependencies](#dependencies)
  * [Other installation methods](#other-installation-methods)
	 * [Ubuntu](#ubuntu)
	 * [Arch-Linux](#arch-linux)
  * [Build](#build)
  * [Compatibility](#compatibility)
  * [FAQ](#faq)


## What it does
* Monitoring your CPU temperature/utilization/frequency/power
* Shows performance dips caused by thermal throttling 
* Requires minimal resources
* Requires no X-server
* Built in options for stressing the CPU (stress/stress-ng)


## Usage
```
s-tui
```
or  
```
sudo s-tui
```

## Simple installation
### pip (x86 + ARM)
```
sudo pip install s-tui
```
Or if you cannot use sudo:
```
pip install s-tui --user
```

If you are installing s-tui on a Raspberry-Pi you might need to install `python-dev` first

### Run local executable (x86 only):
* Download the latest release version from https://github.com/amanusk/s-tui/releases
* Change s-tui to executable `chmod +x s-tui`
* Run `(sudo) ./s-tui`

## Options
```
********s-tui manual********
usage: s_tui.py [-h] [-d] [-c] [-t] [-j] [-nm] [-v] [-ct CUSTOM_TEMP]

TUI interface:

The side bar houses the controls for the displayed grahps.
At the bottom of the side bar, more information is presented in text form.

* Use the arrow keys or 'hjkl' to navigate the side bar
* Toggle between stressed and regular operation using the radio buttons in 'Modes'.
* If you wish to alternate stress defaults, you can do it in 'Stress options'
* Select a different temperature sensors from the 'Temp Sensors' menu
* Change time between updates using the 'Refresh' field
* Use the 'Reset' button to reset graphs and statistics
* Toggle displayed graphs by selecting the [X] check box
* If a sensor is not available on your system, N/A is presented
* If your system supports it, you can use the utf8 button to get a smoother graph
* Press 'q' or the 'Quit' button to quit

* Run `s-tui --help` to get this message and additional cli options

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Output debug log to _s-tui.log
  -c, --csv             Save stats to csv file
  -t, --terminal        Display a single line of stats without tui
  -j, --json            Display a single line of stats in JSON format
  -nm, --no-mouse       Disable Mouse for TTY systems
  -v, --version         Display version
  -ct CUSTOM_TEMP, --custom_temp CUSTOM_TEMP
                        
                        Custom temperature sensors.
                        The format is: <sensors>,<number>
                        As it appears in 'sensors'
                        e.g
                        > sensors
                        it8792-isa-0a60,
                        temp1: +47.0C
                        temp2: +35.0C
                        temp3: +37.0C
                        
                        use: -ct it8792,0 for temp 1

```

## Dependencies
s-tui is a great tool for monitoring. If you would like to stress your computer, install stress. Stress options will then show up in s-tui (optional)
```
sudo apt-get install stress
```

## Other installation methods
### Ubuntu
Installation is available from ppa. Apt does not hold the latest versions of psutil and urwid. Some features will not work.
```
sudo add-apt-repository ppa:amanusk/python-s-tui
sudo apt-get update
sudo apt-get install python-s-tui
```
### Arch-Linux
An AUR package is available called 's-tui'  
Thanks to @DonOregano

## Build
Running s-tui from source  
Clone
```
git clone https://github.com/amanusk/s-tui.git
```
Install libraries   
These need to be installed to run s-tui.py
```
(sudo) pip install urwid
(sudo) pip install psutil
```
Install stress (optional)
```
sudo apt-get install stress
```

Run the .py file
```
(sudo) python -m s_tui.s_tui
```
### OPTIONAL integration of FIRESTARTER (via submodule, does not work on all systems)
FIRESTARTER is a great tool to stress your system to the extreme.  If you would like, you can integrate FIRESTARTER submodule into s-tui.
To build FIRESTARTER  
```
git submodule init
git submodule update
cd ./FIRESTARTER
./code-generator.py
make
```
Once you have completed these steps, you can either:
* Install FIRESTARTER to make it accessible to s-tui, e.g make a soft-link to FIRESTARTER in /usr/local/bin.
* Run s-tui from the main project directory with `python -m s_tui.s_tui`  
An option to run FIRESTARTER will then be available in s-tui

## Compatibility
s-tui uses psutil to probe some of your hardware information. If your hardware is not supported, you might not see all the information.

* On Intel machines:  
Running s-tui as root gives access to the maximum Turbo Boost frequency available to your CPU when stressing all cores.
Running without root will display the Turbo Boost available on a single core. 

* Power read is supported on Intel Core CPUs of the second generation and newer (Sandy Bridge)  
* s-tui tested to run on Raspberry-Pi 3,2,1

## Q&A
__Q__: How is this different from htop?  
__A__: s-tui is not a processes monitor like htop. The purpose is to monitor your CPU statistics and have an option to test the system under heavy load.  (Think AIDA64 stress test, not task manager).  


__Q__: What features require sudo permissions?  
__A__: Top Turbo frequency varies depending on how many cores are utilized. Sudo permissions are required in order to accurately read the top frequency when all the cores are utilized.  


__Q__: I don't have a temperature graph  
__A__: Systems have different sensors to read CPU temperature. If you do not see a temperature read, your system might not be supported (yet). You can try manually setting the sensor with the cli interface (see --help), or selecting a sensor from the  'Temp Sensors' menu


__Q__: I have a temperature graph, but it is wrong.  
__A__: A default sensor is selected for temperature reads. On some systems this sensor might indicate the wrong temperature. You can manually select a sensor from the 'Temp Sensors' menu or using the cli interface (see --help)

__Q__: I am using the TTY with no X server and s-tui crashes on start  
__A__: By default, s-tui is handles mouse inputs. This causes some systems to crash. Try running `s-tui --no-mouse` 
