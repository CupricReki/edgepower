#!/usr/bin/python
import subprocess
import sys
import os
from datetime import datetime
from subprocess import Popen, PIPE

# Skyler Ogden
# This script is design to pull the configs from an existing LED or HID install to update current config files

if len(sys.argv) <= 1:
    # Test to ensure that the user as provided an IP address and site number
    print "For a 3.5 box, an IP address must be specified, the version is assumed." 
    print "Example: python {} 10.77.87.31\n".format(sys.argv[0])
    print "For a 3.3 box, an IP address, and version number must be specified."
    print "Example: python {} 10.77.87.31 3.3".format(sys.argv[0])
    sys.exit()
else:
    # Assign passed arguments to variables
    site_IP = sys.argv[1]
    if len(sys.argv) >= 3 and sys.argv[2] == "3.3":
        site_type = sys.argv[2]
        site_user = "cti"
        config_files = [
            # Place any custom files you want to download here for a site running 3.3
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

    if len(sys.argv) >= 3 and sys.argv[2] != "3.3":
        print "Only version 3.3 and 3.5 are supported"
        sys.exit()

    if len(sys.argv) == 2: 
        site_type = "3.5"
        site_user = "root"
        config_files = [
            # Place any custom files you want to download here for a site running 3.5
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

    # Concatenate all files into a single string to allow for one scp call later
    config_call = " ".join(config_files)

def get_hostname():
    global hostname
    stdout, stderr = Popen(['ssh', 'root@10.77.87.31', 'hostname'], stdout=PIPE).communicate()
    hostname = os.path.splitext(stdout)[1]
    hostname = hostname.rstrip()
    hostname = "{}_".format(hostname.translate(None, '.?'))
    return

def create_config_file():
    # Concatenate the string with the current system timestamp
    global config_dir
    config_dir = "{}configs_{}_{}".format(hostname, site_IP, datetime.now().strftime('%Y%m%d_%H%M%S'))

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
else:
    hostname = ""


create_config_file()
scp_pull()


# TODO:
# Pull the site name back via ssh
# Test with an LED site
# Test with HID sites
# Add auto-detection by -uname -l (2.6 is 3.5, 3.3 is 2.0)
