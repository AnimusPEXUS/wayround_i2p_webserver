#!/usr/bin/python3

import wayround_org.utils.program
import wayround_org.webserver.commands

main = wayround_org.utils.program.MainScript(
    wayround_org.webserver.commands,
    'wrows',
    'INFO'
    ).main

if __name__ == '__main__':
    exit(main())
