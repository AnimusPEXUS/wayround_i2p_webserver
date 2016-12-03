#!/usr/bin/python3

import wayround_i2p.utils.program
import wayround_i2p.webserver.commands

main = wayround_i2p.utils.program.MainScript(
    wayround_i2p.webserver.commands,
    'wrows',
    'INFO'
    ).main

if __name__ == '__main__':
    exit(main())
