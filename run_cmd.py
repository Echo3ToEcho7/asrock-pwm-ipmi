#!/usr/bin/python3
import subprocess as sp

def setSpeed(fan, setspeed):
	speeds, speedsRaw = getAllSpeeds()
	speedcmd = ["ipmitool", "raw", "0x3a", "0x01"]
	for speed in speedsRaw:
		hexspeed = "0x"
		hexspeed += str(speed)
		speedcmd.append(hexspeed)
	speedcmd.append("0x00") # append the mystery (unused) extra values
	speedcmd.append("0x00")
	speedcmd[fan + 3] = hex(setspeed) # index + 3 because the array already has the beginning of the command
	#print(speeds)
	sp.call(speedcmd)

def getAllSpeeds():
	cmdoutput = sp.Popen(["ipmitool", "raw", "0x3a", "0x02"], stdout=sp.PIPE)
	speedsRaw, err = cmdoutput.communicate()
	speedsRaw = str(speedsRaw)[3:20].split()
	speeds = []
	for speed in speedsRaw:
		speeds.append(int(speed, 16))
	return speeds, speedsRaw

def getSpeed(fan):
	speeds, speedsRaw = getAllSpeeds()
	return speeds[fan - 1]

def getFanInfo():
	cmdoutput = sp.Popen(["ipmitool", "sdr"], stdout=sp.PIPE)
	sensorinfo, err = cmdoutput.communicate()
	#print(sensorinfo.splitlines())
	faninfo = []
	speeds, speedsRaw= getAllSpeeds()
	for line in sensorinfo.splitlines():
		if "FAN" in str(line):
			faninfo.append(str(line))
	for index, line in enumerate(faninfo):
		faninfo[index] = str(line)[2:-1]
		faninfo[index] += " | "
		if speeds[index] == 0:
			faninfo[index] += "Auto"
		else:
			faninfo[index] += str(speeds[index])
			faninfo[index] += "%"
		#print(faninfo[index])
	return faninfo
