#!/usr/bin/python3
import run_cmd
import argparse
import time

# Variables to determine bounds
MAXFAN = 6
MINSPEED = 50
MAXSPEED = 100
MINTEMP = 45
MAXTEMP = 65

parser = argparse.ArgumentParser(description='Read information about and control fans on ASRock boards with IPMI.', prog='asrock-pwm-ipmi')
parser.add_argument('fanplusspeed', nargs='*', metavar='FAN:SPEED', help='Fan to change the speed of, and the speed, separated by \':\'. Set to 0 for auto.')
parser.add_argument('-i', '--info',  action="store_true", default=False, help='Read fan information')
parser.add_argument('-a', '--auto',  action="store_true", default=False, help='Service to control fans based on temperature')
parser.add_argument('-q', '--quiet', action="store_true", default=False, help='Hide output')
args = parser.parse_args()

#print(args)

fanChanged = False

def iterateFans(info):
    for fanopt in info:
        if str(fanopt.split(":"))[2:-2] == fanopt or int(fanopt.split(":")[0]) < 1 or int(fanopt.split(":")[0]) > MAXFAN:
            print("Improper format!")
            continue
        fan, speed = fanopt.split(":")
        run_cmd.setSpeed(int(fan), int(speed))
        fanChanged = True
        if args.quiet is False:
            if int(speed) == 0:
                print("Set speed of FAN" + fan + " to Auto.")
            else:
                print("Set speed of FAN" + fan + " to " + speed + "%.")

while args.auto is True:
        temp = run_cmd.getTemp()
        speeds = []
        if temp < MINTEMP:
                speeds.append("3:50")
        elif temp > MAXTEMP:
                speeds.append("3:100")
        else:
                base = temp - MINTEMP
                max = MAXTEMP - MINTEMP
                scaled = base / max
                speed = int(scaled * (MAXSPEED - MINSPEED) + MINSPEED)
                speeds.append("3:" + str(speed))
        iterateFans(speeds)
        time.sleep(2)

if args.info is False and len(args.fanplusspeed) == 0:
        print("Nothing to do! See --help for usage.")
        quit
if len(args.fanplusspeed) != 0:
        iterateFans(args.fanplusspeed)
if args.info is True:
        if fanChanged is True:
                print("\nWaiting for fans to adjust...")
                time.sleep(5)
        print("\nRetrieving fan speeds...\n")
        for line in run_cmd.getFanInfo():
                print(line)
