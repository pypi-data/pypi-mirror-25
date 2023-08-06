#clsBatlab
import serial
import serial.tools.list_ports
from time import sleep, ctime, time
import datetime
import threading
import queue
import sys
import math
import os
try:
	# For Python 3.0 and later
	from urllib.request import urlopen
except ImportError:
	# Fall back to Python 2's urllib2
	from urllib2 import urlopen
import re
###################################################################################################
## Local Functions
###################################################################################################
DEBUG_MODE = None
#DEBUG_MODE = True
def log(str):
	if DEBUG_MODE:
		print(str)
###################################################################################################
## batpool class - manage a pool of connected batlabs by maintaining a list of plugged-in systems
###################################################################################################
class batpool:
	def __init__(self):
		self.msgqueue = queue.Queue()
		self.batpool = dict()
		self.batactive = ''
		self.quitevt = threading.Event()
		thread = threading.Thread(target=self.batpool_mgr)
		thread.daemon = True
		thread.start()
		
	def batpool_mgr(self):
		while(True):
			portlist = get_ports()
			for port in portlist:
				if port not in self.batpool:
					self.batpool[port] = batlab(port)
					self.msgqueue.put('Batlab on ' + port + ' connected')
					if self.batactive == '':
						self.batactive = port
						self.msgqueue.put('Batlab on ' + port + ' set as the Active Batlab')
			for port in list(self.batpool.keys()):
				if port not in portlist:
					self.batpool[port].disconnect()
					del self.batpool[port]
					self.msgqueue.put('Batlab on ' + port + ' disconnected')
			if self.quitevt.is_set():
				for port in list(self.batpool.keys()):
					self.batpool[port].disconnect()
					del self.batpool[port]
				return
			sleep(0.5)
			
	def active_exists(self):
		if self.batactive == '':
			log('No Batlab Currently Set As Active')
			return False
		if self.batactive in self.batpool:
			return True
		else:
			log('Batlab on ' + self.batactive + ' not found')
			return False
			
	def quit(self):
		self.quitevt.set() #tries to tell all of the Batlabs to stop the tests
		sleep(0.5)

###################################################################################################
## packet class - holds information related to usb packets
###################################################################################################
class packet:
	def __init__(self):
		self.valid = True
		self.timestamp = None
		self.namespace = None
		self.type = None
		self.addr = None
		self.data = None
		self.mode = None
		self.status = None
		self.temp = None
		self.voltage = None
		self.current = None
		self.write = None
		self.R = [1500,1500,1500,1500]
		self.B = [3380,3380,3380,3380]
	def set_temps(Rlist,Blist):
		'''deprecated'''
		for i in range(0,4):
			self.R[i] = Rlist[i]
			self.B[i] = Blist[i]
	def value(self):
		if(self.type == 'RESPONSE'):
			return self.data
		else:
			li = [self.mode,self.status,self.temp,self.current,self.voltage]
			return li
	def asvoltage(self):
		if(self.data & 0x8000): #the voltage can be negative
			self.data = -0x10000 + self.data
		flt = float(self.data * 4.5 / 2**15)
		return flt
	def asvcc(self):
		return 2**15 * 4.096 / self.data
	def asfreq(self):
		return self.data * (10000.0 / 256.0)
	def asioff(self):
		return self.data / 128.0
	def assetpoint(self):
		return self.data / 128.0
	def asmagdiv(self):
		return 2.0 / (2 ** self.data)
	def asmode(self):
		try:
			return MODE_LIST[self.data]
		except:
			return 'MODE_UNKNOWN'
	def aserr(self):
		for i in range(0,6):
			if self.data & (1 << i):
				return ERR_LIST[i]
			return 'ERR_NONE'
	def astemperature(self):
		Rdiv = self.R[self.namespace]
		R = Rdiv / ((2**15 / self.data)-1)
		To = 25 + 273.15
		Ro = 10000
		B = self.B[self.namespace] #3380
		Tinv = (1 / To) + (math.log(R/Ro) / B)
		T = (1 / Tinv) - 273.15
		T = (T * 1.8) + 32
		return T
	def astemperature(self,Rlist,Blist):
		Rdiv = Rlist[self.namespace]
		R = Rdiv / ((2**15 / self.data)-1)
		To = 25 + 273.15
		Ro = 10000
		B = Blist[self.namespace] #3380
		Tinv = (1 / To) + (math.log(R/Ro) / B)
		T = (1 / Tinv) - 273.15
		T = (T * 1.8) + 32
		return T
	def ascurrent(self):
		if(self.data & 0x8000): #the current can be negative
			self.data = -0x10000 + self.data
		return self.data * 4.096 / 2**15
	def print_packet(self):
		if(self.type == 'RESPONSE'):
			if self.write == True:
				log('Wrote: Cell '+str(self.namespace)+', Addr '+"{0:#4X}".format(self.addr & 0x7F))
			else:
				log('Read: Cell '+str(self.namespace)+', Addr '+"{0:#4X}".format(self.addr & 0x7F)+': '+str(self.data))
	def display(self):
		if(self.type == 'RESPONSE'):
			if self.write == True:
				print('Wrote: Cell '+str(self.namespace)+', Addr '+"{0:#4X}".format(self.addr & 0x7F))
			else:
				print('Read: Cell '+str(self.namespace)+', Addr '+"{0:#4X}".format(self.addr & 0x7F)+': '+str(self.data))	

###################################################################################################
## encoder class - given value, converts to register data. essentially the opposite of packet class
###################################################################################################
class encoder:
	def __init__(self,data):
		self.data = data
	def asvoltage(self):
		return int(self.data * 2**15 / 4.5)
	def asvcc(self):
		return  int((2**15 * 4.096)  / self.data)
	def asfreq(self):
		return int(self.data / (10000.0 / 256.0))
	def asioff(self):
		return int(self.data * 128.0)
	def assetpoint(self):
		return int((self.data * 128))
	def asmagdiv(self):
		return int(1 - math.log2(self.data))
	def ascurrent(self):
		return int(self.data * 2**15 / 4.096)
	def aschargel(self):
		return  ((self.data * 9.765625 / 4.096 / 6) * 2**15) & 0xFFFF
	def aschargeh(self):
		return  ((self.data * 9.765625 / 4.096 / 6) * 2**15) >> 16
	def astemperature(self,Rdiv,B):
		To = 25 + 273.15
		Ro = 10000
		F = (self.data - 32) / 1.8
		F = 1/(F + 273.15)
		R = math.exp((F - (1 / To)) * B) * Ro
		if (R > 0 and Rdiv > 0):
			R = (2**15)/(((1/R)*Rdiv) + 1)
		else:
			R = -100 # dummy value
		return int(R)
###################################################################################################
def ascharge(data):
	return ((6 * (data / 2**15) ) * 4.096 / 9.765625)		
###################################################################################################
## Holds an instance of 1 Batlab. Pass in a COM port
###################################################################################################
class batlab:
###################################################################################################
	def __init__(self,port=None):
		self.sn = '' #deprecated
		self.ver = '' #deprecated
		self.port = port
		self.is_open = False
		self.qstream = queue.Queue()   #Queue of stream packets
		self.qresponse = queue.Queue() #Queue of response packets
		self.killevt = threading.Event()
		self.B = [3380,3380,3380,3380]
		self.R = [10000,10000,10000,10000]
		self.connect()
###################################################################################################
	def connect(self):
		while True:
			try:
				self.ser = serial.Serial(None,38400,timeout=1)
				self.ser.port = self.port
				self.ser.close()
				self.ser.open()
			except:
				#self.reset_port()
				#continue
				log("Could not connect to port")
				return -1
			break
		self.is_open = self.ser.is_open
		thread = threading.Thread(target=self.thd_read) #start receiver thread
		thread.daemon = True
		thread.start()
		if self.read(0x05,0x01).value() == 257: #then we're not in the bootloader
			self.write(UNIT,SETTINGS,SET_TRIM_OUTPUT)
			self.R[0] = self.read(0x00,0x16).data
			self.R[1] = self.read(0x01,0x16).data
			self.R[2] = self.read(0x02,0x16).data
			self.R[3] = self.read(0x03,0x16).data
			self.B[0] = self.read(0x00,0x17).data
			self.B[1] = self.read(0x01,0x17).data
			self.B[2] = self.read(0x02,0x17).data
			self.B[3] = self.read(0x03,0x17).data
			a = self.read(0x04,0x00).data 
			b = self.read(0x04,0x01).data
			self.sn = str(a + b*65536)
			self.ver = str(self.read(0x04,0x02).data)
		else:
			log("The Batlab is in the bootloader")
###################################################################################################
	def disconnect(self):
		self.killevt.set()
		self.ser.close()
###################################################################################################
	def set_port(self,port):
		try:
			self.ser.port = port
			self.connect()
			return 1
		except:
			return 0
###################################################################################################
	'''	
		def reset_port(self):
			portinfos = serial.tools.list_ports.comports()
			for portinfo in portinfos:
				print(portinfo.device + ' ' + str(portinfo.vid) + ' ' + str(portinfo.pid))
				if(portinfo.vid == 0x04D8 and portinfo.pid == 0x000A and portinfo.device == self.ser.port):
					devname = 'DevManView /disable_enable "' + portinfo.description +'"'
					print("Resetting COM port "+devname)
					call(devname,shell=True)
					return
			print("Device not found...")
			return
	'''
###################################################################################################
	def read(self,namespace,addr):
		if not (namespace in NAMESPACE_LIST):
			print("Namespace Invalid")
			return None
		try:
			q = packet()
			outctr = 0
			while(True):
				self.ser.write((0xAA).to_bytes(1,byteorder='big'))
				self.ser.write(namespace.to_bytes(1,byteorder='big'))
				self.ser.write(addr.to_bytes(1,byteorder='big'))
				self.ser.write((0x00).to_bytes(1,byteorder='big'))
				self.ser.write((0x00).to_bytes(1,byteorder='big'))
				self.ser.flush()
				ctr = 0
				while(self.qresponse.qsize() == 0 and ctr < 50):
					sleep(0.001)
					ctr = ctr + 1
				while(self.qresponse.qsize() > 0):
					q = self.qresponse.get()
				if( (q.addr == addr and q.namespace == namespace) ): #or outctr > 20 ):
					return q
				if outctr > 50:
					q.valid = False
					return q
				outctr = outctr + 1
		except:
			return None
###################################################################################################
	def write(self,namespace,addr,value):
		if not (namespace in NAMESPACE_LIST):
			print("Namespace Invalid")
			return None
		if value > 65535 or value < -65535:
			print("Invalid value: 16 bit value expected")
			return None
		if(value & 0x8000): #convert large numbers into negative numbers because the to_bytes call is expecting an int16
			value = -0x10000 + value
			
		try:
			q = None
			outctr = 0
			namespace = int(namespace)
			addr = int(addr)
			value = int(value)
			while(True):
				self.ser.write((0xAA).to_bytes(1,byteorder='big'))
				self.ser.write(namespace.to_bytes(1,byteorder='big'))
				self.ser.write((addr | 0x80).to_bytes(1,byteorder='big'))
				self.ser.write(value.to_bytes(2, byteorder='little',signed=True))
				self.ser.flush()
				ctr = 0
				while(self.qresponse.qsize() == 0 and ctr < 50):
					sleep(0.001)
					ctr = ctr + 1
				while(self.qresponse.qsize() > 0):
					q = self.qresponse.get()
				if( q.addr == addr and q.namespace == namespace ):
					return q
				if( outctr > 20 ):
					q.valid = False
					return q
				outctr = outctr + 1
		except:
			return None
###################################################################################################
## get_stream - retrieve stream packet from queue
###################################################################################################
	def get_stream(self):
		q = None
		while self.qstream.qsize() > 0:
			q = self.qstream.get()
		return q
###################################################################################################
## Macros
###################################################################################################
	def set_current(self,cell,current):
		self.write(cell,CURRENT_SETPOINT,int((current/5.0)*640))
	def sn(self):
		a = self.read(UNIT,0x00).data 
		b = self.read(UNIT,0x01).data
		return a + b*65536
	def ver(self):
		return self.read(0x04,0x02).data
###################################################################################################
	def firmware_bootload(self,filename):
			'''Check to make sure image is at least the right size'''
			try:
				with open(filename, "rb") as f:
					sz = os.path.getsize(f.name)
					if not (sz == 15360):
						print("Image filesize of",sz,"not allowed")
						return False
			except:
				print("Could not open file")
				return False
			'''command the Batlab to enter the bootloader'''
			print("Entering Bootloader")
			self.write(UNIT,BOOTLOAD,0x0000)
			sleep(2)
			'''load the image onto the batlab'''
			with open(filename, "rb") as f:
				byte = f.read(1)
				ctr = 0x0400
				while byte:
					self.write(BOOTLOADER,BL_ADDR,int(ctr))
					self.write(BOOTLOADER,BL_DATA,int(ord(byte)))
					bb = self.read(BOOTLOADER,BL_DATA).value()
					if(bb != int(ord(byte))):
						log("Data Mismatch. Trying again")
						continue
					print(str(ctr - 0x03FF) + " of 15360: " + str(bb) ) 
					ctr = ctr + 1
					byte = f.read(1)
			'''attempt to reboot into the new image'''
			self.write(BOOTLOADER,BL_BOOTLOAD,0x0000)
			sleep(2)
			if(self.read(BOOTLOADER,BL_DATA).value() == COMMAND_ERROR):
				self.sn = int(self.read(UNIT,SERIAL_NUM).value()) + (int(self.read(UNIT,DEVICE_ID).value()) << 16)
				print("Connected to Batlab " + str(self.sn))
				fw = int(self.read(UNIT,FIRMWARE_VER).value())
				print("Firmware Version " + str(fw))
				return True
			else:
				print("Batlab still in Bootloader -- Try again")
				return False
###################################################################################################
	def firmware_check(self,flag_download):
		# Download latest version and get version number
		urlpath =urlopen('https://github.com/Lexcelon/batlab-firmware-measure/releases/latest/')
		string = urlpath.read().decode('utf-8')
		pattern = re.compile('/[^/]*\.bin"') #the pattern actually creates duplicates in the list
		filelist = pattern.findall(string)
		#print(filelist)
		filename = filelist[0]
		versionlist = re.findall(r'\d+', filename)
		#print(versionlist)
		version = int(versionlist[0])
		pattern = re.compile('".*\.bin"') #the pattern actually creates duplicates in the list
		filelist2 = pattern.findall(string)
		#print(filelist2)
		filename2 = filelist2[0]
		#print(filename2)
		filename2=filename2[:-1]
		filename2=filename2[1:]
		filename=filename[:-1]
		filename=filename[1:]
		if flag_download == True:
			#print('https://github.com' + filename2)
			remotefile = urlopen('https://github.com' + filename2)
			localfile = open(filename,'wb')
			localfile.write(remotefile.read())
			localfile.close()
			remotefile.close()
		#print("Latest firmware version is:",version)
		return [version,filename]
###################################################################################################
	def firmware_update(self):
		version,filename = self.firmware_check(True)
		loadedver = self.read(UNIT,FIRMWARE_VER).data
		print("Latest Version is",version,". Current version is",loadedver)
		if(version > loadedver):
			print("Initiating Firmware Update")
			sleep(2)
			self.firmware_bootload(filename)
		else:
			print("Firmware is up to date.")
###################################################################################################
###################################################################################################
###################################################################################################
## Reading thread - parses incoming packets and adds them to queues
###################################################################################################
	def thd_read(self):
		while True:
			if self.killevt.is_set(): #stop the thread if the batlab object goes out of scope
				return
			val = None
			try:
				val = self.ser.read()
			except:
				return
			if(val):
				inbuf = []
				ctr = 0
				byte = ord(val)
				if(byte == 0xAA): #Command Response Byte 1: 0xAA
					while (len(inbuf) < 4 and ctr < 20):
						for b in self.ser.read():
							inbuf.append(b)
						ctr = ctr + 1
					if ctr == 20:
						continue
					p = packet()
					p.timestamp = datetime.datetime.now()
					p.type = 'RESPONSE'
					p.namespace = inbuf[0]
					if((inbuf[1] & 0x80)):       #Command Response Byte 3:  w/~r + addr
						p.write = True
					p.addr = inbuf[1] & 0x7F   
					p.data = inbuf[2] + inbuf[3]*256  #data payload
					self.qresponse.put(p)                     #Add the packet to the queue
					p.print_packet()
				elif(byte == 0xAF): #stream packet Byte 1: 0xAF
					while len(inbuf) < 12 and ctr < 20:
						for b in self.ser.read():
							inbuf.append(b)
						ctr = ctr + 1
					if ctr == 20:
						continue
					p = packet()
					p.timestamp = datetime.datetime.now()
					p.namespace = inbuf[0]
					if(inbuf[1] == 0):
						p.type = 'STREAM'
						p.mode = inbuf[2] + inbuf[3] * 256
						p.status = inbuf[4] + inbuf[5] * 256
						p.temp = inbuf[6] + inbuf[7] * 256
						p.current = inbuf[8] + inbuf[9] * 256
						p.voltage = inbuf[10] + inbuf[11] * 256
					self.qstream.put(p)                     #Add the packet to the queue
					p.print_packet()
				else:
					log("<<thdBatlab:Packet Loss Detected>>")
###################################################################################################
###################################################################################################
###################################################################################################
## Global Functions
###################################################################################################
def get_ports():
	portinfos = serial.tools.list_ports.comports()
	port = []
	for portinfo in portinfos:
		log(portinfo)
		log(portinfo.device + ' ' + str(portinfo.vid) + ' ' + str(portinfo.pid))
		if(portinfo.vid == 0x04D8 and portinfo.pid == 0x000A):
			log("found Batlab on "+portinfo.device)
			port.append(portinfo.device)
	return port
###################################################################################################
'''namespace definitions'''
CELL0             = 0x00
CELL1             = 0x01
CELL2             = 0x02
CELL3             = 0x03
UNIT              = 0x04
BOOTLOADER        = 0x05
COMMS             = 0xFF
NAMESPACE_LIST = [0x00,0x01,0x02,0x03,0x04,0x05,0xFF]
'''cell register map'''
MODE              = 0x00
ERROR             = 0x01
STATUS            = 0x02
CURRENT_SETPOINT  = 0x03
REPORT_INTERVAL   = 0x04
TEMPERATURE       = 0x05
CURRENT           = 0x06
VOLTAGE           = 0x07
CHARGEL           = 0x08
CHARGEH           = 0x09 
VOLTAGE_LIMIT_CHG = 0x0A
VOLTAGE_LIMIT_DCHG= 0x0B
CURRENT_LIMIT_CHG = 0x0C
CURRENT_LIMIT_DCHG= 0x0D
TEMP_LIMIT_CHG    = 0x0E
TEMP_LIMIT_DCHG   = 0x0F
DUTY              = 0x10
COMPENSATION      = 0x11
CURRENT_PP        = 0x12
VOLTAGE_PP        = 0x13
CURRENT_CALIB_OFF = 0x14
CURRENT_CALIB_SCA = 0x15
TEMP_CALIB_R      = 0x16
TEMP_CALIB_B      = 0x17
CURRENT_CALIB_PP  = 0x18
VOLTAGE_CALIB_PP  = 0x19
CURR_CALIB_PP_OFF = 0x1A
VOLT_CALIB_PP_OFF = 0x1B
CURR_LOWV_SCA     = 0x1C
CURR_LOWV_OFF     = 0x1D
CURR_LOWV_OFF_SCA = 0x1E

CELLREG_MAX = 0x1E
'''unit register map'''
SERIAL_NUM       =  0x00
DEVICE_ID        =  0x01
FIRMWARE_VER     =  0x02
VCC              =  0x03
SINE_FREQ        =  0x04
SYSTEM_TIMER     =  0x05
SETTINGS         =  0x06
SINE_OFFSET      =  0x07
SINE_MAGDIV      =  0x08
LED_MESSAGE      =  0x09
BOOTLOAD         =  0x0A
VOLT_CH_CALIB_OFF = 0x0B
VOLT_CH_CALIB_SCA = 0x0C
VOLT_DC_CALIB_OFF = 0x0D
VOLT_DC_CALIB_SCA = 0x0E
LOCK              = 0x0F
ZERO_AMP_THRESH   = 0x10

UNITREG_MAX = 0x10
'''COMMs register map'''
LED0             = 0x00
LED1             = 0x01
LED2             = 0x02
LED3             = 0x03
PSU              = 0x04
PSU_VOLTAGE      = 0x05

COMMREGS_MAX = 0x05
'''BOOTLOAD register map'''
BL_BOOTLOAD      = 0x00
BL_ADDR          = 0x01
BL_DATA          = 0x02
'''register specific codes and defines'''
MODE_NO_CELL           = 0x0000
MODE_BACKWARDS         = 0x0001
MODE_IDLE              = 0x0002
MODE_CHARGE            = 0x0003
MODE_DISCHARGE         = 0x0004
MODE_IMPEDANCE         = 0x0005
MODE_STOPPED           = 0x0006
MODE_LIST = ['MODE_NO_CELL','MODE_BACKWARDS','MODE_IDLE','MODE_CHARGE','MODE_DISCHARGE','MODE_IMPEDANCE','MODE_STOPPED']
ERR_VOLTAGE_LIMIT_CHG  = 0x0001
ERR_VOLTAGE_LIMIT_DCHG = 0x0002
ERR_CURRENT_LIMIT_CHG  = 0x0004
ERR_CURRENT_LIMIT_DCHG = 0x0008
ERR_TEMP_LIMIT_CHG     = 0x0010
ERR_TEMP_LIMIT_DCHG    = 0x0020
ERR_LIST = ['ERR_VOLTAGE_LIMIT_CHG','ERR_VOLTAGE_LIMIT_DCHG','ERR_CURRENT_LIMIT_CHG','ERR_CURRENT_LIMIT_DCHG','ERR_TEMP_LIMIT_CHG','ERR_TEMP_LIMIT_DCHG']
STAT_VOLTAGE_LIMIT_CHG = 0x0001
STAT_VOLTAGE_LIMIT_DCHG= 0x0002
STAT_CURRENT_LIMIT_CHG = 0x0004
STAT_CURRENT_LIMIT_DCHG= 0x0008
STAT_TEMP_LIMIT_CHG    = 0x0010
STAT_TEMP_LIMIT_DCHG   = 0x0020
STAT_BACKWARDS         = 0x0040
STAT_NO_CELL           = 0x0080
SET_TRIM_OUTPUT        = 0x0001
SET_VCC_COMPENSATION   = 0x0002
SET_DEBUG              = 0x8000
LED_OFF                = 0x0000 
LED_BLIP               = 0x0001
LED_FLASH_SLOW         = 0x0002
LED_FLASH_FAST         = 0x0003
LED_ON                 = 0x0004
LED_PWM                = 0x0005
LED_RAMP_UP            = 0x0006
LED_RAMP_DOWN          = 0x0007
LED_SINE               = 0x0008

LOCK_LOCKED            = 0x0001
LOCK_UNLOCKED          = 0x0000

COMMAND_ERROR          = 257
###################################################################################################
