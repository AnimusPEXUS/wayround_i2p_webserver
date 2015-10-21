
import collections

import wayround_org.webserver.webserver


def commands():
    ret = collections.OrderedDict([
        ('server', collections.OrderedDict([
            ('start', server_start),
        ]))
    ])
    return ret


def server_start(command_name, opts, args, adds):
    ret = 0
    serv = wayround_org.webserver.webserver.WebServer(
        #'/etc/wrows.conf'
        '/home/agu/_local/p/wayround_org_webserver/trunk/test/wrows.conf'
        )
    serv.start()
    serv.wait_for_shutdown()
    return ret
