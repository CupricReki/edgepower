#!/usr/bin/python
import subprocess
import sys
import os
from datetime import datetime
from subprocess import Popen, PIPE

# Skyler Ogden
# This script is design to pull the configs from an existing LED or HID install to update current config files

if len(sys.argv) <= 2:
    # Test to ensure that the user as provided an IP address and site number
    print "This script requires an IP address and an EnFlex version number"
    print "Example: python {} 10.77.87.31 3.5".format(sys.argv[0])
    print "Example with optional directory: python {} 10.77.87.31 3.5".format(sys.argv[0])
    sys.exit()
else:
    # Assign passed arguments to variables
    site_IP = sys.argv[1]
    site_type = sys.argv[2]

    if site_type == "3.5":
        config_files = [
            # Place any custom files you want to download here for LED sites
            "/var/www/enflex-user/costco/html/config/siteconfig*.js",
            "/home/enflex/drivers/scheduler/scheduler_config.txt",
            "/home/enflex/drivers/lightingled/lightingled_config.txt",
            "/home/enflex/drivers/acuity/acuity_config.txt",
            "/home/enflex/drivers/acuity/acuity_fixture_definitions.txt",
            "/home/enflex/drivers/modbus/ADAM4019.txt",
            "/home/enflex/drivers/modbus/H*.txt",
            "/home/enflex/drivers/input-broker/input_broker_config.xml"
            "/home/enflex/drivers/modbus/PM*.txt",
            "/home/enflex/drivers/base/sensor*.txt"
        ]
        site_user = "root"
    elif site_type == "3.3":
        config_files = [
            # Place any custom files you want to download here
            "/home/httpd/docs/config/siteconfig*.js",
            "/home/cti/db/esl/trane",
            "/home/cti/drivers/base/sensor*.txt",
            "/home/cti/drivers/summit/summit_config.txt",
            "/home/cti/drivers/summit/schedule_names.txt",
            "/home/cti/drivers/input-broker/input_broker_config.xml",
            "/home/cti/drivers/modbus/H*.txt",
            "/home/cti/drivers/modbus/ION*",
            "/home/cti/drivers/modbus/CM*",
            "/home/cti/drivers/modbus/ADAM*",
            "/home/cti/drivers/lighting/lighting_config.txt"
        ]
        site_user = "cti"
    else:
        print "This script is only capable of pulling configurations from either 3.3 or 3.5 software"

    # Concatenate all files into a single string to allow for one scp call later
    config_call = " ".join(config_files)

def get_hostname():
    global hostname
    stdout, stderr = Popen(['ssh', 'root@10.77.87.31', 'hostname'], stdout=PIPE).communicate()
    base, hostname = os.path.splitext(stdout)
    hostname = hostname.rstrip()
    hostname = hostname.translate(None, '.?')
    print hostname
    return

def create_config_file():
    # Concatenate the string with the current system timestamp
    global config_dir
    config_dir = "{}_configs_{}_{}".format(hostname, site_IP, datetime.now().strftime('%Y%m%d_%H%M%S'))

    # Create the timestamped folder
    subprocess.call(['mkdir', config_dir])
    return


def scp_pull():
    # Uses scp to pull each file into the timestamped directory
    subprocess.call([
        "scp",
        '{}@{}:{}'.format(site_user, site_IP, config_call),
        config_dir
    ])
    return

if site_type == "3.5":
    get_hostname()

create_config_file()
scp_pull()


# TODO:
# Pull the site name back via ssh
# Test with an LED site
# Test with HID sites
# Add auto-detection by -uname -l (2.6 is 3.5, 3.3 is 2.0)
