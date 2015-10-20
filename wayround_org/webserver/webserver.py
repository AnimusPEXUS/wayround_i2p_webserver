
import threading

import wayround_org.http.message

import wayround_org.webserver.config
import wayround_org.webserver.socket
import wayround_org.webserver.domain


class WebServer:

    def __init__(
            self,
            config_filepath
            ):

        self._config_filepath = config_filepath

        self.socket_pool = None
        self.domain_pool = None

        return

    def start(self):

        cfg = wayround_org.webserver.config.read_from_fs(self._config_filepath)

        self.socket_pool = wayround_org.webserver.socket.Pool(
            cfg,
            callable_target_for_socket_pool
            )
        self.domain_pool = wayround_org.webserver.domain.Pool(cfg)

        self.socket_pool.connect_domains(domain_pool)

        return

    def stop(self):
        self.socket_pool.stop()
        self.domain_pool.stop()
        return

    def wait(self):
        return

    def callable_target_for_socket_pool(
            self,
            transaction_id,
            serv,
            serv_stop_event,
            sock,
            addr,
            ws_socket_inst
            ):

        error = False
        ws_domain_inst = None

        (header_bytes, line_terminator,
            request_line_parsed, header_fields,
            error) = wayround_org.http.message.read_and_parse_header(sock)

        host_field_value = ws_socket_inst.default_domain
        host_field_value_client_provided = False

        for i in header_fields:
            if i[0].lower() == 'host':
                host_field_value = i[1]
                host_field_value_client_provided = True
                break

        if host_field_value is None:
            self.error_socket_shutdown(
                sock,
                wayround_org.http.message.HTTPResponse(
                    500,
                    None,
                    "Internal Server Error: "
                    "not configured default and "
                    "not Host request field provided"
                    )
                )
            error = True

        if not error:
            if host_field_value is not None:
                if not host_field_value in ws_socket_inst.domains:
                    self.error_socket_shutdown(
                        sock,
                        wayround_org.http.message.HTTPResponse(
                            500,
                            None,
                            "Internal Server Error: "
                            "requested Host not served by this socket"
                            )
                        )
                    error = True

        if not error:
            ws_domain_inst = ws_socket_inst.domains[host_field_value]

            t = threading.Thread(
                target=ws_domain_inst.module_inst.callable_for_webserver,
                args=(
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
                    )
                )
            t.start()

        return

    def error_socket_shutdown(self, sock, http_response):
        http_response.send_into_socket(sock)
        sock.shutdown(socket.SHUT_WR)
        sock.close()
        return
