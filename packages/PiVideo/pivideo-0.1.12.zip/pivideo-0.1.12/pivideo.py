#!/usr/bin/python

######################################################################
#
#  PiVideo control program
#  Copyright(c) 2016, 2017 by Lintest Systems LLC
#
######################################################################
#
#  Revision History
#	0.1.2	Initial Released Version
#	0.1.3	Serial port handling changed to support Raspberry Pi 3
#	0.1.4	Parameter processing bug fixed
#	0.1.5	Support for PiCapture HD1
#	0.1.6	Improved HD1 communications
#   0.1.8	Changes for control firmware update; display PiVideo version number on query
#	0.1.9	Improved handling for communication errors in pivideo_class
#	0.1.10	Updated for Python3 compatibility; bug fix for "command"
#	0.1.11	Fix firmware update issue with Python3; Added custom EDID for HD1
#	0.1.12	Improved firmware update features; require future for Python 2
#

from __future__ import print_function 

from builtins import chr
import argparse
import serial
import os
import time
import sys
import subprocess
try:
		import smbus
		_i2c_available = True
except:
		_i2c_available = False
import pivideo_class
sys.tracebacklimit = 0

PiVideo_Version='PiVideo Version 1.12'

#---------------------------------------------------------------------------------
def main():
	switch_values=['off','on']	

	queries=['all','ready','running','lock','source','effect','led','version','id','cmd','skip']
	
	parser = argparse.ArgumentParser(description='PiVideo control program version 0.1.11 -- Lintest Systems LLC')
	parser.add_argument('--verbose','-v',action='count',help='Trace communications with with video processor')
	parser.add_argument('--port','-p',default='i2c1',choices=pivideo_class.ports,help='Specify the communication port for the video processor')
	parser.add_argument('--address','-a',help='Specify the address used for the selected port')
	parser.add_argument('--source','-s',choices=pivideo_class.sources,help='Select the source input')
	parser.add_argument('--skip','-skip',choices=switch_values,help='Frame skip to reduce the capture rate')
	parser.add_argument('--query','-q-',choices=queries,help='Query the status of the video processor')
	parser.add_argument('--effect','-e',choices=pivideo_class.effects,help='Select special effect or test video')
	parser.add_argument('--led','-l',choices=pivideo_class.led_settings,help='Control LED status display')
	parser.add_argument('--edid','-edid',default='_ignore',nargs='?',help='Set custom EDID from file, or reset HDMI connection if no argument')
	parser.add_argument('--update','-update',help='Update the PiVideo firmware')
	parser.add_argument('--force','-force',help='Force update using downlevel PiVideo firmware')
	parser.add_argument('--config','-c',choices=pivideo_class.config_actions,help='Save settings as the power-on default')
	parser.add_argument('--command','-cmd',help='RESERVED')
	parser.add_argument('--script','-script',help='Process a Lintest-supplied script file')
	
	args = parser.parse_args()
	actioncount = 0
	
	if args.query:
		if args.verbose:
			print(PiVideo_Version)			
			
	# Check for OS support installed
	if not _check_os_camera_support():
		print("Make sure camera support is enabled on your system")

	if args.verbose:
		print("Port used for video processor is: ",args.port)

	# Establish communication with the video processor
	vid=pivideo_class.PiVideo()
	vid.pivideo_port=args.port
	if (vid.pivideo_port=="serial"):
		if args.verbose:
			print("Serial device address is ",vid.pivideo_serial_dev)			
		if args.address:
			vid.pivideo_serial_dev=args.address
	else:
		if (_i2c_available==True):
			if args.address:
				vid.pivideo_i2c_address=args.address
		else:
			print("Python smbus module not found - install to use I2C communication")

	try:	
		pivideo_port=vid.open
	except pivideo_class.PiVideoException as e:
		print("Video Processor was not found - please check your jumpers and settings")
		print(e)
	else:	# Process the commands
	
		if (pivideo_port == "loader"):
			if (vid.model == 'SD1'):
				print("PiCapture SD1 is waiting for firmware programming")
			else:
				print("PiCapture HD1 is waiting for firmware programming")
			if args.update:
				actioncount+=1		
				Update_Firmware(vid,args.update,False)
		else:	
	
			if args.source:
				actioncount+=1
				vid.source=args.source
				if args.verbose:
					print("Source is: ",args.source)
		
			if args.effect:
				actioncount+=1
				vid.effect=args.effect
				if args.verbose:
					print("Effect set: ",args.effect)
					
			if args.skip:
				actioncount+=1		
				if (vid.model=='HD1'):
					vid.skip=(args.skip!=switch_values[0])
					if vid.skip:
						print("Frame skip set:  On")
					else:
						print("Frame skip set:  Off")
				else:
					print("--skip option is only for the PiCapture HD1")
	
			if args.led:
				actioncount+=1		
				vid.led=args.led
				if args.verbose:
					print("LED setting is: ",args.led)
		
			if args.config:
				actioncount+=1		
				vid.config=args.config
				if args.verbose:
					print("Configuration:	 ",args.config)
		
			if args.query:
				actioncount+=1
				result=vid.ready
				if (args.query=='all') | (args.query=='ready'):
					print("PiCapture",vid.model,"is ",end='');
					if result:
						print("ready")
					else:
						print("NOT READY")
				if (args.query=='all') | (args.query=='lock'):
					result=vid.lock
					if (result>0):
						print("Active video:  Mode",result)
					else:
						print("No active video detected")
				if (args.query=='all'):
					print("Selected video source is: ",vid.source)
				if (args.query=='all') | (args.query=='source'):
					result=vid.active_source
					print("Active video source is: ",result)
				if (args.query=='all') | (args.query=='running'):
					result=vid.running
					if result:
						print("Raspberry Pi camera port is active")
					else:
						print("Raspberry Pi camera port is not active")
				if (args.query=='all') | (args.query=='effect'):
					result=vid.effect
					if not result=='none':
						if (result=='colorbar'):
							print("Effect set to Color Bars")
						if (result=='bw'):
							print("Effect set to Black & White")
				if (args.query=='all') | (args.query=='skip'):
					if (vid.model=='HD1'):
						if vid.skip:
							print ("Frame skip is On")
						else:
							if (args.query=='skip') | (args.verbose==1):
								print("Frame skip is Off")
					else:
						if (args.query=='skip'):
							print("Frame skip is Off (HD1 only)")
				if (args.query=='all') | (args.query=='led'):
					result=vid.led
					if not result=='normal':
						if (result=='min'):
							print("Basic LED display")
						if (result=='off'):
							print("LEDs off")
					else:
						if (args.query=='led'):
							print("Normal LED display")
				if (args.query=='all') | (args.query=='version'):
					if (args.verbose==1):
						result=vid.version+"-"+vid.long_version
					else:
						result=vid.version
					print("Video processor firmware version: ",result)
				if ((args.query=='all') & (args.verbose==1)) | (args.query=='id'):
					result=vid.id
					print("Video processor hardware id: ",result)
				if (args.query=='cmd'):
					result=vid.command
					print("",result)
	
			if (args.edid!='_ignore'):
				actioncount+=1
				edid_control(vid,args.edid)
	
			if args.update:
				actioncount+=1		
				Update_Firmware(vid,args.update,False)
	
			if args.force:
				actioncount+=1		
				Update_Firmware(vid,args.force,True)
		
			if args.command:
				actioncount+=1		
				vid.command=args.command
				if (len(args.command)==8):
					print("Command result:  ",vid.command)
		
			if args.script:
				actioncount+=1		
				Process_Script(vid,args.script)
				
			if (actioncount == 0):
				print("For a complete list of options use 'pivideo --help'")


#----------------------------------------------------------------------
# HD1 EDID control

def edid_control(vid,filename):
	if (vid.model=='HD1'):
		if (filename):
			try:
				edidfile=open(filename)
			except:
				print("EDID file not found")
			else:
				filesize=os.stat(filename).st_size	
				if (filesize==256):
					edid_data=[]
					while 1:
						bvalue = edidfile.read(1)
						if not bvalue:
							break
						edid_data += [bvalue]
					vid.edid=edid_data
				else:
					print("EDID files must be exactly 256 bytes")
				edidfile.close();
		else:
			vid.edid=[]
	else:
		print("--edid option is only for the PiCapture HD1")


#----------------------------------------------------------------------
# Check for OS camera support installed

def _check_os_camera_support():
	try:
		ossupport = os.popen('vcgencmd get_camera').readline()
	except:
		return False
	else:
		if (ossupport.count("=1")>=1):	# return value should be "supported=1 detected=1"
			return True
		else:
			return False
		
#----------------------------------------------------------------------
# Clear serial buffer

def _clear_serial_buffer(vid):
	lastchar=" "
	while (lastchar!=""):
		lastchar=vid.serport.read(1)

#----------------------------------------------------------------------
# UPDATE FIRMWARE

def Update_Firmware(vid,filename,force):
	vid._check_video_open()
	if (vid.status in ["i2c0","i2c1"]):
		print("Firmware update is only supported over serial connection")
	else:
		fileopen = False
		try:
			updatefile=open(filename)
		except:
			print("Update file not found")
		else:
			fileopen = True
			hexfilesize=os.stat(filename).st_size
			fccount=0
			success=True
			print()
			print("Updating firmware from file ",filename)
			print("Update file size is ",hexfilesize)
			print()
			_clear_serial_buffer(vid)
			for line in updatefile:
				if (line[0:2]=="LT"):
					if (fccount==0):
						fccount=3
						if (vid.status == "loader"):
							if (vid.model == "SD1"):
								uv1=int("0"+line[2:4],16)
								if ((uv1 & 0x80) == 0):
									if (uv1 < 0x07):
										print("Firmware update error:  version not compatible with bootloader")
										break
								else:
									print("Firmware update error:  PiCapture HD firmware not compatible with PiCapture SD")
									break
							else:
								uv1=int("0"+line[2:4],16)
								if ((uv1 & 0x80) == 0x80):
									if ((uv1 & 0x7F) < 0x07):
										print("Firmware update error:  version not compatible with bootloader")
										break
								else:
									print("Firmware update error:  PiCapture SD firmware not compatible with PiCapture HD")
									break						
						else:
							cversion=vid.long_version
							cv1=int(cversion[0:2],16) & 127
							cv2=int(cversion[2:4],16) & 192
							cv3=int(cversion[4:6],16)
							uv1=int("0"+line[2:4],16) & 127
							uv2=int("0"+line[4:6],16) & 192
							uv3=int("0"+line[6:8],16)
							if (uv1<=cv1):
								print("Warning: update file version is not newer than the current version")
								if not force:
									print("Use -force to fall back to an earlier version")
									success=False
									break
							elif (uv2!=cv2):
								print("Firmware update error:  video engine version mismatch")
								success=False
								break
							elif (uv3!=cv3):
								print("Firmware update error:  incompatible version")
								success=False
								break
							elif ((cv1 < 6) & (uv1 > 6)):
								print("Firmware update error:  must upgrade bootloader before update");
								success=False;
								break 
						print("DO NOT INTERRUPT THE FIRMWARE UPDATE PROCESS!")
						vid.update
						_clear_serial_buffer(vid)
					else:
						print("Not a valid PiCapture update file")
						success=False
						break;
				elif (line[0]=="#"):
					print(line[1:])
				elif (line[0]==':'):
					tryagain=True
					while (tryagain):
						lccount=0
						for character in line:
							lccount+=1
							if (ord(character)!=10):
								vid.serport.write(character)
						time.sleep(0.2)
						while (vid.serport.inWaiting()>0):
							a=vid.serport.read(1)
							if (ord(a)==6):
								tryagain=False
					_clear_serial_buffer(vid)
					fccount+=lccount
					percent=int((fccount*100/hexfilesize)+0.5)
					sys.stdout.write("\rFirmware update in progress:  %d%%" % percent)
					sys.stdout.flush()
			if success:
				print("\rUpdate complete - video processor will now restart")
			else:
				print("\rUpdate was not completed						   ")
		finally:
			print()
			if fileopen:
				updatefile.close()

#----------------------------------------------------------------------
# PROCESS SCRIPT

def Process_Script(vid,filename):
	vid._check_video_open()
	try:
		scriptfile=open(filename);
	except:
		raise PiVideoException("Script file not found")
	else:
		success=True
		print()
		print("Processing script file ",filename)
		print()
		for line in scriptfile:
			if (line[0]=="#"):
				print(line[1:])
			elif (line[0]==","):
				time.sleep(len(line)*0.1)
			elif (len(line)>=16):
				vid.command=line[0:16]
			else:
				print("Invalid script entry:  ",line)
	finally:
		print()
		scriptfile.close()

#----------------------------------------------------------------------

if __name__ == "__main__":
		main()
