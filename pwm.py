#!/usr/bin/python3
import run_cmd
import argparse

MAXFAN = 6

parser = argparse.ArgumentParser(description='Read information about and control fans on ASRock boards with IPMI.', prog='asrock-pwm-ipmi')
parser.add_argument('fanplusspeed', nargs='*', metavar='FAN:SPEED',
                   help='Fan to change the speed of, and the speed, separated by \':\'. Set to 0 for auto.')
#parser.add_argument('SPEED', type=int, nargs='+',
#                   help='Speed to set FAN to')
parser.add_argument('-i', '--info', action="store_true", default=False,
                   help='Read fan information')


args = parser.parse_args()
#print(args.info)
#print(args)
#print(args.fanplusspeed)
if args.info is False and args.fanplusspeed == []:
	print("Nothing to do! See --help for usage.")
	quit
if args.fanplusspeed != []:
	for fanopt in args.fanplusspeed:
		if str(fanopt.split(":"))[2:-2] == fanopt or int(fanopt.split(":")[0]) < 1 or int(fanopt.split(":")[0]) > MAXFAN:
			print("Improper format!")
			continue
		fan, speed = fanopt.split(":")
		run_cmd.setSpeed(int(fan), int(speed))
		if int(speed) == 0:
			print("Set speed of FAN" + fan + " to Auto.")
		else:
			print("Set speed of FAN" + fan + " to " + speed + "%.")
if args.info is True:
	print("\nRetrieving fan speeds...\n")
	for line in run_cmd.getFanInfo():
		print(line)
