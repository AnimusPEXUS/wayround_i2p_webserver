
import importlib
import logging

"""

module structure description:
    wayround_org_webserver domain module must have 2 strict things:
        1. class named 'WebServerModule', which has following
           parameters:
            1. reference to webserver instance;
            2. reference to socket pool
            3. reference to domain pool
            last. dict with parameters passed from configuration file
        2. WebServerModule class instances must have callable methods:
            1. 'callable_for_webserver' which must have following parameters:
                # first part of parameters
                #     parameters passed by SocketServer
                transaction_id,
                serv,
                serv_stop_event,
                sock,
                addr,

                # second part of parameters 
                #     WebServer socket and domain instances
                ws_socket_inst,
                ws_domain_inst,

                # third part of parameters 
                #     header parsing result (as WebServer reads and parses 
                #     header manually to retrive Host parameter)
                header_bytes,
                line_terminator,
                request_line_parsed,
                header_fields
            2. 'start' - called on domain start() called
            3. 'stop' - called on domain stop() called
            4. 'wait' - called on domain wait() called
"""

class Domain:
    """

    this class (or it's instances) is not intended for direct initialization.

    it's created, used and destroyed by DomainPool class instance
    """

    def __init__(
            self,
            domain_data_dict,
            web_server_inst,
            domain_pool_inst
            ):
        self.name = domain_data_dict['name']
        self.domain = domain_data_dict['domain']
        self.module = domain_data_dict['module']
        self.module_inst = None
        self._load_module(web_server_inst, domain_pool_inst)

        self._web_server_inst = web_server_inst
        self._domain_pool_inst = domain_pool_inst

        return

    def _load_module(self, web_server_inst):
        """
        result: True - Ok, False - Error
        """

        ret = True

        module = None

        module_name = 'wayround_org.webserver.mudules.{}'.format(self.name)

        try:
            module = importlib.import_module(module_name)
        except:
            logging.exception(
                "Error loading module `{}'".format(module_name)
                )
            ret = False

        if ret:

            if not hasattr(module, 'WebServerModule'):
                logging.exception(
                    "module `{}' has no WebServerModule member".format(
                        module_name
                        )
                    )
                ret = False

        if ret:
            self.module_inst = module.WebServerModule(
                web_server_inst
                )

        return ret

    def start(self):
        return

    def stop(self):
        # NOTE: probably there will no be actual stoppers, as webserver
        #       lifetime, most probably, will be oneshot.
        #       but there is still probability what some WSGI
        #       site implimentations will require special preperations
        #       before stop.
        #
        #       shortly saying: I'm not sure is stop() method needed here
        #                       but it will be called by WebServer at it's
        #                       life end.
        return


class DomainPool:

    def __init__(self):
        self._storage = {}
        return

    def load_domains(domain_data_dict_lst):
        """
        result: True - Ok, False - Error
        """
        ret = True

        for i in domain_data_dict_lst:
            d = Domain(i)
            self._storage[d.name]=d

        return ret

    def find_by_name(self, name):
        return self._storage.get(name, None)

    def find_by_domain(self, domain):

        ret = None

        for i in list(self._storage.values()):
            if i.domain == domain:
                ret.append(i)

        return ret
