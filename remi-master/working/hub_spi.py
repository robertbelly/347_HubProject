#!usr/bin/python

#Shawn Martin
#6/7/18
#EECS 347-2

import spidev
import time

SPI_RESPONSE_DELAY_SEC = 0.07		#Delay for BT to store response in buffer
SPI_MESSAGE_DELAY_SEC = 0.05		#Delay between subsequent messages
BUFFER_SIZE = 16			#Maximum buffer size

MAX_ATTEMPTS = 3			#Maximum number of times sending will be attempted
SHOW_STATS = True 			#If stats debug info required

PAIRING_DURATION = 60			#Seconds that pairing will be active until timeout
PAIRING_SCAN_DELAY = 2			#Seconds between index refresh during pairing

invalid_index = True			#If index requested is invalid
index_val = -1				#Highest valid index

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 8000000		#SPI Speed (8MHz)

string_ascii = []
output_str = []
valid_message = True

successful_messages = 0.00
total_messages = 0.00
loop_times = 0

EOT_CHAR = ";"

COMMAND_INDEX = "q"
COMMAND_GET = "g"
COMMAND_SET = "s"
COMMAND_PAIR = "pair"
COMMAND_DELETE = "d"

CHAR_UUIDS = "uuids"
CHAR_ONOFF = "onoff"
CHAR_BATTERY = "batte"
CHAR_ANALOG_OUT = "anout"
CHAR_ANALOG_MAX = "anmax"
CHAR_ANALOG_MIN = "anmin"

RESPONSE_SUCCESS = str("1" + EOT_CHAR)
RESPONSE_NO_SUCCESS = str("0" + EOT_CHAR)
RESPONSE_INVALID = str("i" + EOT_CHAR)
RESPONSE_ERROR = str("e" + EOT_CHAR)
RESPONSE_NO_INDEX = str("n" + EOT_CHAR)

CATEGORY_ON_OFF = "on_off"
CATEGORY_SENSOR = "sensor"
CATEGORY_UNKNWN = "unknwn"

device_uuids = ["", "", "", "", "", "", "", ""]
device_on_off = [0, 0, 0, 0, 0, 0, 0, 0]
device_battery = [0, 0, 0, 0, 0, 0, 0, 0]
device_analog_out = [0, 0, 0, 0, 0, 0, 0, 0]
device_analog_thresh = [0, 0, 0, 0, 0, 0, 0, 0]
device_analog_max = [0, 0, 0, 0, 0, 0, 0, 0]
device_analog_min = [0, 0, 0, 0, 0, 0, 0, 0]


def send_string(spi_str):
	"Sends a string over SPI, stores in output_str."

	global total_messages
	global successful_messages
	global output_str

	output = [0 for x in range(BUFFER_SIZE)]

	valid_message = True
	
	string_ascii = [ord(c) for c in spi_str]
	data = string_ascii

	print(">>>Out: " + str(data) + " (" + str(spi_str) + ")")
	spi.xfer(data)

	time.sleep(SPI_RESPONSE_DELAY_SEC)

	output = spi.xfer(data)
	output_str = ''.join(chr(i) for i in output)

	output_eot = output_str.find(';')
	
	if output_eot < 0:
		valid_message = False

	output_str = output_str[:output_eot+1]

	print(">>>In: " + str(output) + " (" + str(output_str) + ")")

	total_messages += 1

	if valid_message:
		successful_messages += 1

	return valid_message

def attempt_send_x_times(spi_str, times):
	"Will send and receive a string message. Safe due to finite duration."

	success = True

	valid_message = False
	counter = 0

	if(spi_str == ""):
		success = False
		counter = times

	while (valid_message != True and counter < times):
		valid_message = send_string(spi_str)
		counter += 1
		if(valid_message != True and counter < times):
			time.sleep(SPI_MESSAGE_DELAY_SEC)

	if(counter >= times and valid_message != True):
		success = False

	return success

def pack_command(command, module_index, characteristic, variable):
	"Packs command into string for SPI sending."

	if(command == COMMAND_INDEX):
		full_str = str(command + EOT_CHAR)
	elif(command == COMMAND_PAIR):
		full_str = str(command + EOT_CHAR)
	elif(command == COMMAND_SET):
		full_str = str(command) + " " + str(module_index) + "." + str(characteristic) + " " + str(variable) + EOT_CHAR
	elif(command == COMMAND_GET):
		full_str = str(command) + " " + str(module_index) + "." + str(characteristic) + EOT_CHAR + "   "
	elif(command == COMMAND_DELETE):
		full_str = str(command) + " " + str(module_index) + EOT_CHAR
	else:
		print("Invalid command.")
		full_str = ""

	return full_str

def check_invalid_index():
	"Returns true if index does not exist -- false otherwise."

	return(str(output_str) == RESPONSE_NO_INDEX)

def check_invalid():
	"Returns true if invalid command received."

	return(str(output_str) == RESPONSE_INVALID)

def check_error():
	"Returns true if error is module response."
	
	return(str(output_str) == RESPONSE_ERROR)

def set_fail():
	"Returns true if response is 0; -- false otherwise."

	return(str(output_str) == RESPONSE_NO_SUCCESS)

def set_success():
	"Returns true if response is 1; -- false otherwise."

	return(str(output_str) == RESPONSE_SUCCESS)

def check_get(characteristic, module_index):
	"If input is GET response, check validity, set values if valid."

	value = output_str[:len(output_str)-1]

	if(characteristic == CHAR_UUIDS):
		if(not check_invalid()):
			device_uuids[module_index] = str(value)
			return True
	elif(characteristic == CHAR_ONOFF):
		if(set_success() or set_fail() and not check_invalid()):
			try:
				device_on_off[module_index] = int(value)
				return True
			except ValueError:
				return False
	elif(characteristic == CHAR_BATTERY):
		if(not check_invalid()):
			try:
				batt = int(value)
				if(batt >= 0 and batt <= 100):
					device_battery[module_index] = batt
				return(batt >= 0 and batt <= 100)
			except ValueError:
				return False
	elif(characteristic == CHAR_ANALOG_OUT):
		if(not check_invalid()):
			try:
				device_analog_out[module_index] = float(value)
				return True
			except ValueError:
				return False

	return False

def check_index():
	"Stores number of devices in index_val."

	global index_val

	index = 0

	output_eot = output_str.find(';')

	index = str(output_str[:output_eot])

	if(int(index) >= 0):
		index_val = int(index) - 1
		#print("index: " + str(index_val))
		return True

	return False

def send_over_SPI(attempts, command, module_index, characteristic, variable):
	"Sends a command over SPI. Handles sending and response."

	if(module_index < 0):
		print("Invalid index.")
		return False

	spi_str = pack_command(command, module_index, characteristic, variable)

	counter = 0
	complete = False

	while(counter < attempts and complete == False):
		success = attempt_send_x_times(spi_str, 1)
		counter += 1
		if(check_invalid_index()):
			print("Invalid index.")
			counter = attempts
			success = False
		elif(check_error()):
			print("Module returned error.")
			success = False
			complete = True
		elif(success): #valid EoT
			if(command == COMMAND_INDEX and check_invalid() == False):
				if(check_index()):
					complete = True
			if(command == COMMAND_SET and check_invalid() == False):
				if(set_success()):
					complete = True
			if(command == COMMAND_GET and check_invalid() == False):
				complete = check_get(characteristic, module_index)	
			if(command == COMMAND_PAIR and check_invalid() == False):
				if(set_success()):
					complete = True
			if(command == COMMAND_DELETE and check_invalid() == False):
				if(set_success()):
					complete = True

		if(check_invalid() == True or check_invalid_index() == True):
			complete = False
			print("Check invalid = true in new_value_set, command = " + str(command))
		time.sleep(SPI_MESSAGE_DELAY_SEC)

	if(complete == True):
		#print("Completed successfully.")
		invalid_index = False
	else:
		print("Completed unsuccessfully, index = " + str(module_index) + " command = " + str(command) + " char = " + str(characteristic))

	return complete

def get_index():
	"Stores highest index into index_val."

	send_over_SPI(MAX_ATTEMPTS, COMMAND_INDEX, 0, 0 ,0)
	time.sleep(SPI_MESSAGE_DELAY_SEC)

	return True

def get_uuid(module_index):
	"Puts UUID of index into device array."

	if(module_index < 0 or module_index > index_val):
		print("Invalid index.")
		return False

	send_over_SPI(MAX_ATTEMPTS, COMMAND_GET, module_index, CHAR_UUIDS, 0)
	time.sleep(SPI_MESSAGE_DELAY_SEC)

	return True

def read_chars(module_index):
	"Gets all variables from module."

	if(module_index < 0 or index_val < 0):
		return False

	send_over_SPI(MAX_ATTEMPTS, COMMAND_GET, module_index, CHAR_ONOFF, 0)
	time.sleep(SPI_MESSAGE_DELAY_SEC)
	send_over_SPI(MAX_ATTEMPTS, COMMAND_GET, module_index, CHAR_BATTERY, 0)
	time.sleep(SPI_MESSAGE_DELAY_SEC)
	send_over_SPI(MAX_ATTEMPTS, COMMAND_GET, module_index, CHAR_ANALOG_OUT, 0)
	time.sleep(SPI_MESSAGE_DELAY_SEC)

	print("Finished reading all chars from module " + str(module_index))

	return True

def print_module(module_index):
	"Prints all characteristics of module."

	if(module_index > index_val):
		return False

	print("")
	print("Module #:  " + str(module_index))
	print("UUID:      " + device_uuids[module_index])

	category = device_uuids[module_index]

	if(len(category) > 10):
		category = category[11]
		category_print = ""

		if(category == "o"):
			category_print = CATEGORY_ON_OFF
		elif(category == "s"):
			category_print = CATEGORY_SENSOR
		else:
			category_print = CATEGORY_UNKNWN

		print("Category:  " + str(category_print))
	else:
		print("Cannot print category.")

	print("-----------------------")
	print("On Off:    " + str(device_on_off[module_index]))
	print("Battery:   " + str(device_battery[module_index]))
	print("An. Out:   " + str(device_analog_out[module_index]))
	print("An. Thres: " + str(device_analog_thresh[module_index]))
	print("An. Max:   " + str(device_analog_max[module_index]))
	print("An. Min:   " + str(device_analog_min[module_index]))
	print("")

	return True

def print_all_modules():
	"Prints all characteristics of all modules."

	if(index_val < 0):
		print("No module info to print.")
		return False

	for x in range(0, index_val+1):
		print_module(x)

	return True

def check_analog_threshold(module_index):
	"Returns true if analog threshold reached"

	thresh_reached = False

	if(device_analog_out[module_index] > device_analog_max[module_index]):
		print("Analog out > analog max")
		device_analog_thresh[module_index] = 1
		thresh_reached = True
	if(device_analog_out[module_index] < device_analog_min[module_index]):
		print("Analog out < analog min")
		device_analog_thresh[module_index] = 1
		thresh_reached = True

	return thresh_reached

def start_pair():
	"Sends pair command."

	print("Starting pair process")
	send_over_SPI(MAX_ATTEMPTS, COMMAND_PAIR, 0, 0, 0)
	time.sleep(SPI_MESSAGE_DELAY_SEC)

	return True

def init_table():
	"Clears table, refills (gets) device information."

	device_uuids = ["", "", "", "", "", "", "", ""]
	device_on_off = [0, 0, 0, 0, 0, 0, 0, 0]
	device_battery = [0, 0, 0, 0, 0, 0, 0, 0]
	device_analog_out = [0, 0, 0, 0, 0, 0, 0, 0]
	device_analog_thresh = [0, 0, 0, 0, 0, 0, 0, 0]
	device_analog_max = [0, 0, 0, 0, 0, 0, 0, 0]
	device_analog_min = [0, 0, 0, 0, 0, 0, 0, 0]

	get_index()

	if(index_val >= 0):
		for x in range(0, index_val+1):
			get_uuid(x)
			read_chars(x)

	return True

def check_uuid():
	"If UUID has changed (at all, including order), repopulate table with correct values."
	
	get_index()

	if(index_val >= 0):
		temp_uuid = ""
		for x in range(0, index_val+1):
			temp_uuid = device_uuids[x]
			get_uuid(x)
			if(device_uuids[x] != temp_uuid):
				init_table()
				return True

	return False

def new_value_set(module_index, characteristic, value):
	"Sets value into characteristic of module_index, sends over SPI. Returns True if successful, False otherwise."

	if(module_index < 0 or index_val < 0):
		print("Invalid index.")
		return False

	if(characteristic == CHAR_ONOFF):
		if(value == 0 or value == 1):
			try:
				device_on_off[module_index] = int(value)
				send_over_SPI(MAX_ATTEMPTS, COMMAND_SET, module_index, CHAR_ONOFF, device_on_off[module_index])
				time.sleep(SPI_MESSAGE_DELAY_SEC)
				return True
			except ValueError:
				print("Invalid value")
				return False
		else:
			print("Invalid value")
			return False
	elif(characteristic == CHAR_ANALOG_MAX):
		try:
			device_analog_max[module_index] = float(value)
			send_over_SPI(MAX_ATTEMPTS, COMMAND_SET, module_index, CHAR_ANALOG_MAX, device_analog_max[module_index])
			time.sleep(SPI_MESSAGE_DELAY_SEC)
			return True
		except ValueError:
			print("Invalid value")
			return False
	elif(characteristic == CHAR_ANALOG_MIN):
		try:
			device_analog_min[module_index] = float(value)
			send_over_SPI(MAX_ATTEMPTS, COMMAND_SET, module_index, CHAR_ANALOG_MIN, device_analog_min[module_index])
			time.sleep(SPI_MESSAGE_DELAY_SEC)
			return True
		except ValueError:
			print("Invalid value")
			return False
	else:
		print("Invalid characteristic.")
		return False

def delete_index(module_index):
	"Deletes index from table on all devices."

	if(module_index < 0 or module_index > index_val):
		print("Invalid index")
		return False

	send_over_SPI(MAX_ATTEMPTS, COMMAND_DELETE, module_index, 0, 0)
	time.sleep(SPI_MESSAGE_DELAY_SEC)

	print("Index " + str(module_index) + " deleted.")

	init_table()

	return True

def init_pairing():
	"Starts pairing process. If new device found, table refreshed."

	temp_index_val = index_val

	start_pair()

	for x in range(0, PAIRING_DURATION):
		print("Attempting to pair. " + str(PAIRING_DURATION - x) + " seconds until timeout.")
		time.sleep(PAIRING_SCAN_DELAY)
		get_index()
		if(index_val > temp_index_val):
			print("Found device. Stopped pairing process.")
			init_table()
			return True

	print("No new devices paired. Pairing process failed due to timeout.")
	return False


#Start Main Function

init_table() #fill table with info

# time.sleep(3)
#
# init_pairing()
#
# time.sleep(1)
#
# new_value_set(0, CHAR_ONOFF, 1)
#
# time.sleep(2)
#
# read_chars(0)
#
# while True:
#
# 	read_chars(0)
# 	check_uuid()
#
# 	print_all_modules()
#
# 	if(SHOW_STATS):
# 		loop_times += 1
# 		print("Successful messages: " + str(successful_messages))
# 		print("Total messages:      " + str(total_messages))
# 		print("Loop times:          " + str(loop_times))
# 		if(total_messages > 0):
# 			ratio = successful_messages/total_messages * 100
# 			avg_loops = total_messages/loop_times
# 			print("Success rate:        " + str(ratio) + "%")
# 			print("Average per loop:    " + str(avg_loops))
#
# 		print("")
#
# spi.close()
# print("Finished SPI")

#End Main Function