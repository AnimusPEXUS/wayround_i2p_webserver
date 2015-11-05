
import socket
import ssl

import wayround_org.socketserver.server

import wayround_org.webserver.application


class SocketSSL:
    """

    this class (or it's instances) is not intended for direct use.
    it should be used throug Socket instances which has non-None .ssl
    attribute
    """

    def __init__(self, socket_data_dict):
        self.keyfile = None
        if 'keyfile' in socket_data_dict:
            self.keyfile = socket_data_dict['keyfile']

        self.certfile = socket_data_dict['certfile']
        return


class Socket:
    """

    this class (or it's instances) is not intended for direct initialization.

    it's created, used and destroyed by SocketPool class instance
    """

    def __init__(self, socket_data_dict, callable_target):
        self.name = socket_data_dict['name']
        self.address = socket_data_dict['address']
        self.port = socket_data_dict['port']
        self.application_names = socket_data_dict['application_names']
        self.default_application_name = socket_data_dict['default_application_name']

        if not isinstance(self.application_names, list):
            raise Exception(
                "configuration: socket config parameter `application_names' "
                "values must be list of strings"
                )

        self.ssl = None
        if 'SSL' in socket_data_dict:
            self.ssl = SocketSSLCfg(socket_data_dict['name'])

        self.applications = {}

        self.socket_server = None
        self.socket = None

        self._callable_target = callable_target

        return

    def connect_applications(self, application_pool):
        application_names_to_load = self.application_names
        if self.default_application_name is not None:
            application_names_to_load += [self.default_application_name]

        application_names_to_load = list(set(application_names_to_load))

        for i in application_names_to_load:

            dom = application_pool.get_by_name(i)
            if dom is None:
                raise Exception("application pool has no name `{}'".format(i))

            if dom.domain in self.domains:
                raise Exception(
                    "socket: `{}:{}' already have domain `{}'".format(
                        self.address,
                        self.port,
                        dom.domain
                        )
                    )
            self.domains[dom.domain] = dom

        return

    def start(self):

        s = None

        if self.ssl:
            s = ssl.SSLSocket(
                server_side=True,

                keyfile=self.ssl.keyfile,
                certfile=self.ssl.certfile

                # TODO: need conf
                # cert_reqs=CERT_NONE,
                # ssl_version={see docs},
                # ciphers=None

                # ca_certs=None,
                # do_handshake_on_connect=True,
                # suppress_ragged_eofs=True,
                )
        else:
            s = socket.socket()

        if s is None:
            raise Exception("Programming error")

        s.setblocking(False)
        try:
            s.bind((self.address, self.port))
        except OSError as err:
            if err.args[0] == 98:
                print("Tryed to bind port on address: {}".format(self.address))
            raise

        self.socket = s

        s.listen(5)  # TODO: configure for this argument

        self.socket_server = wayround_org.socketserver.server.SocketServer(
            s,
            self.target
            )
        self.socket_server.start()
        return

    def stop(self):
        if self.socket:
            self.socket.shutdown(socket.SHUT_WR)
            self.socket.close()
        if self.socket_server:
            self.socket_server.stop()
        return

    def wait(self):
        # TODO
        return

    def target(
            self,
            transaction_id,
            serv,
            serv_stop_event,
            sock,
            addr
            ):

        self._callable_target(
            transaction_id,
            serv,
            serv_stop_event,
            sock,
            addr,
            self
            )

        return


class Pool:

    def __init__(self, cfg, callable_target):
        self._socket_pool = []
        for i in cfg['sockets']:
            self._socket_pool.append(Socket(i, callable_target))
        return

    def connect_applications(self, application_pool):
        for i in self._socket_pool:
            i.connect_applications(application_pool)
        return

    def start(self):
        for i in self._socket_pool:
            i.start()
        return

    def stop(self):
        for i in self._socket_pool:
            i.stop()
        return

    def wait(self):
        for i in self._socket_pool:
            i.wait()
        return
