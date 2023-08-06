#!/usr/bin/env python
"""Mookfist LimitlessLED Control

This tool can be used to control your LimitlessLED based lights.

Usage:
    lled.py fade <start> <end> (--group=<GROUP>)... [options]
    lled.py fadec <start> <end> (--group=<GROUP>)... [options]
    lled.py fadeb <startb> <endb> <startc> <endc> (--group=<GROUP>)... [options]
    lled.py on (--group=<group>)... [options]
    lled.py off (--group=<group>)... [options]
    lled.py color <color> (--group=<GROUP>)... [options]
    lled.py colorcycle (--group=<GROUP>)... [options]
    lled.py rgb <r> <g> <b> (--group=<GROUP>)... [options]
    lled.py white (--group=<GROUP>)... [options]
    lled.py brightness <brightness> (--group=<GROUP>)... [options]
    lled.py scan [options]

Options:
    -h --bridge-ip=HOST       IP / Hostname of the bridge
    -p --bridge-port=PORT     Port number of the bridge (defaults to 8899 or 5987)
    --bridge-version=VERSION  Bridge version (defaults to 4)
    -g GROUP --group=GROUP    Group number (defaults to 1)
    --bulb=BULB               Bulb type
    -r RC --repeat=RC         Number of times to repeat a command
    --pause=PAUSE             Number of milliseconds to wait between commands
    --debug                   Enable debugging output
    -h --help                 Show this help
    --help-bulbtypes          Display possible bulb type values
"""
import logging
from docopt import docopt

from mookfist_lled_controller.cli import configure_logger
from mookfist_lled_controller.cli import Main

def main():
    """Main function!"""
    arguments = docopt(__doc__, version='Mookfist LimitlessLED Control 0.1.0')
    configure_logger(arguments['--debug'])

    log = logging.getLogger('lled')

    log.info('Welcome to the Mookfist LimitlessLED Controller')

    try:
        m = Main(arguments)
        m.run()
    except KeyboardInterrupt:
        log.warning('Stopping')


if __name__ == '__main__':
    main()
