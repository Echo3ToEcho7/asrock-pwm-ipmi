# Custom version
This fork is updated to work with most recent BIOS and BMC. My needs are to watch my NVidia Tesla T4 that has a PWM fan connected to FAN3, so the auto function looks only at the NVidia SMI Temp and the speed of FAN3.

# asrock-pwm-ipmi

This is a script to control 4-pin PWM fans on ASRock Rack motherboards with IPMI. The BMC does not properly expose fan control, so they must be controlled using raw IPMI commands. This script is a user-friendly way to do that.


    usage: asrock-pwm-ipmi [-h] [-i] [-a] [-q] [FAN:SPEED [FAN:SPEED ...]]

    Read information about and control fans on ASRock boards with IPMI.

    positional arguments:
      FAN:SPEED   Fan to change the speed of, and the speed, separated by ':'. Set
                  to 0 for auto.

    optional arguments:
      -h, --help   show this help message and exit
      -i, --info   Read fan information
      -a, --auto   Service to control fans based on temperature
      -q, --quiet  Hide output
  
