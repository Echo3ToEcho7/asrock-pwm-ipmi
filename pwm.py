#!/usr/bin/python3
import run_cmd
import argparse
import time
MAXFAN = 6
MINSPEED = 35
MAXSPEED = 100
MINTEMP = 30
MAXTEMP = 65

parser = argparse.ArgumentParser(description='Read information about and control fans on ASRock boards with IPMI.', prog='asrock-pwm-ipmi')
parser.add_argument('fanplusspeed', nargs='*', metavar='FAN:SPEED',
                   help='Fan to change the speed of, and the speed, separated by \':\'. Set to 0 for auto.')
#parser.add_argument('SPEED', type=int, nargs='+',
#                   help='Speed to set FAN to')
parser.add_argument('-i', '--info', action="store_true", default=False,
                   help='Read fan information')
parser.add_argument('-a', '--auto', action="store_true", default=False,
		   help='Service to control fans based on temperature')

args = parser.parse_args()
#print(args.info)
#print(args)
#print(args.fanplusspeed)
fanChanged = False

def iterateFans(info):
	for fanopt in info:
                if str(fanopt.split(":"))[2:-2] == fanopt or int(fanopt.split(":")[0]) < 1 or int(fanopt.split(":")[0]) > MAXFAN:
                        print("Improper format!")
                        continue
                fan, speed = fanopt.split(":")
                run_cmd.setSpeed(int(fan), int(speed))
                fanChanged = True
                if int(speed) == 0:
                        print("Set speed of FAN" + fan + " to Auto.")
                else:
                        print("Set speed of FAN" + fan + " to " + speed + "%.")


while args.auto is True:
	temp = run_cmd.getTemp()
	speeds = []
	if temp < MINTEMP:
		for i in range(2, 7):
			speeds.append(str(i) + ":1")
		#speeds = "2:1 3:1 4:1 5:1 6:1"
	elif temp > MAXTEMP:
		for i in range(2, 7):
                	speeds.append(str(i) + ":100")
		#speeds = "2:100 3:100 4:100 5:100 6:100"
	else:
		base = temp - MINTEMP
		max = MAXTEMP - MINTEMP
		scaled = base / max
		speed = int(scaled * (MAXSPEED - MINSPEED) + MINSPEED)
		for i in range(2, 7):
                	speeds.append(str(i) + ":" + str(speed))
	iterateFans(speeds)
	#print(speeds)
	#time.sleep(1)

if args.info is False and args.fanplusspeed == []:
	print("Nothing to do! See --help for usage.")
	quit
if args.fanplusspeed != []:
	iterateFans(args.fanplusspeed)
if args.info is True:
	if fanChanged is True:
		print("\nWaiting for fans to adjust...")
		time.sleep(5)
	print("\nRetrieving fan speeds...\n")
	for line in run_cmd.getFanInfo():
		print(line)
