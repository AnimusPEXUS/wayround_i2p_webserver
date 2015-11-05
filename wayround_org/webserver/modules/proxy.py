
import logging
import select
import socket
import threading
import time
import gc

import wayround_org.http.message


def proxify_socket(one, another, name, stop_event):
    data = None
    while True:
        if stop_event.is_set():
            break
        data = None
        while True:
            if stop_event.is_set():
                break
            try:
                data = one.recv(4096)
            except BlockingIOError:
                pass
            else:
                break

        if data is None:
            stop_event.set()
            break

        if len(data) == 0:
            stop_event.set()
            break

        while True:
            try:
                another.sendall(data)
            except BlockingIOError:
                pass
            else:
                break

    stop_event.set()

    return


class WebServerModule:

    def __init__(
            self,
            ws_inst,
            socket_pool,
            domain_pool,
            config_params
            ):
        """
        parameters:

          address - domain name or IP
          port    - port number
        """
        self.remote_address = config_params['address']
        self.remote_port = config_params['port']
        self.host_value = config_params['host_value']

        self.on_start = None
        if 'on_start' in config_params['on_start']:
            _t = config_params['on_start']

            self.on_start = {
                'gid': _t.get('gid', None),
                'uid': _t.get('uid', None),
                'command': _t.get('command', None),
                'args': _t.get('args', None),
                'cwd': _t.get('cwd', None)
                }

        self._proc = None

        self.gid = None
        self.uid = None

        return

    def start(self):
        if self.on_start is not None:

            # checking uid and gid

            _t = self.on_start

            self.gid = None
            self.uid = None

            try:
                self.gid = _t['gid']
            except KeyError:
                pass

            try:
                self.uid = _t['uid']
            except KeyError:
                pass

            if self.gid:

                if isinstance(self.gid, str):
                    if self.gid.isnumeric():
                        self.gid = int(self.gid)
                    else:
                        self.gid = grp.getgrnam(self.gid)[2]

                os.setregid(self.gid, self.gid)

            if self.uid:

                if isinstance(self.uid, str):
                    if self.uid.isnumeric():
                        self.uid = int(self.uid)
                    else:
                        self.uid = pwd.getpwnam(self.uid)[2]

                os.setreuid(self.uid, self.uid)

            # starting process

            cmd = []

            if self.gid or self.uid:
                su_cmd = ['su', '-l']

                if self.gid:
                    su_cmd += ['-g', str(self.gid)]

                if self.uid:
                    su_cmd += [str(self.uid)]

                cmd += su_cmd

            cmd += [_t['command']]

            if _t['args']:
                cmd += _t['args']

            print("starting: {}".format(' '.join(cmd)))

            self._httpd_process = subprocess.Popen(
                cmd,
                cwd=_t['cwd'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
                )

        return

    def stop(self):
        if self.on_start is not None:
            if self._proc is not None:
                self._proc.terminate()
        return

    def wait(self):
        if self.on_start is not None:
            self.on_start.wait()
        return

    def callable_for_webserver(
            self,
            transaction_id,
            serv,
            serv_stop_event,
            sock,
            addr,

            ws_socket_inst,
            ws_domain_inst,

            header_bytes,
            line_terminator,
            request_line_parsed,
            header_fields
            ):

        remote_socket = socket.socket()
        remote_socket.setblocking(False)

        while True:
            try:
                remote_socket.connect(
                    (self.remote_address, self.remote_port)
                    )
            except BlockingIOError:
                pass
            except:
                raise
            else:
                break

        for i in range(len(header_fields)):
            if header_fields[i][0] == b'Host':
                header_fields[i] = (b'Host', bytes(self.host_value, 'utf-8'))

        http_req = wayround_org.http.message.HTTPRequest(
            transaction_id,
            serv,
            serv_stop_event,
            sock,
            addr,
            request_line_parsed,
            header_fields
            )

        http_req2 = wayround_org.http.message.ClientHTTPRequest(
            http_req.method,
            http_req.requesttarget,
            http_req.header_fields,
            ''
            )

        reassembled_header_bytes = http_req2.format_header() + line_terminator

        remote_socket.send(reassembled_header_bytes)

        stop_event = threading.Event()

        th1 = threading.Thread(
            target=proxify_socket,
            args=(sock, remote_socket, '->', stop_event)
            )

        th2 = threading.Thread(
            target=proxify_socket,
            args=(remote_socket, sock, '<-', stop_event)
            )

        th1.start()
        th2.start()

        th1.join()
        th2.join()

        gc.collect()

        return
