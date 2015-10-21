
import yaml
import logging

DOMAIN_KEYS = ['name', 'domain', 'module']
DOMAIN_KEYS_OPT = ['module_parameters']

SOCKET_KEYS = ['name', 'address', 'port', 'domain_names', 'default_domain_name']
SOCKET_KEYS_OPT = ['SSL']

SSL_KEYS = ['certfile']
SSL_KEYS_OPT = ['keyfile']


def read_from_fs(filename):

    ret = None

    with open(filename) as f:
        txt = f.read()

    loaded = yaml.load(txt)

    res = correctness_check(loaded)

    if res == False:
        ret = None
    else:
        ret = loaded

    return loaded


def _correctness_check_domain(data_dict, domain):

    ret = True

    if ret:
        if not isinstance(domain, dict):
            logging.error("configuration: domain configuration must be dict")
            ret = False

    if ret:
        for i in DOMAIN_KEYS:
            if not i in domain:
                logging.error(
                    "configuration: domain config requires `{}' key".format(
                        i
                        )
                    )
                ret = False

        for i in list(domain.keys()):
            if not i in DOMAIN_KEYS and not i in DOMAIN_KEYS_OPT:
                logging.error(
                    "configuration: unknown "
                    "key (`{}') found in domain config".format(
                        i
                        )
                    )
                ret = False

    # NOTE and TODO: here most likely mest be more checks

    return ret


def _correctness_check_socket(data_dict, socket):

    ret = True

    if ret:
        if not isinstance(socket, dict):
            logging.error("configuration: socket configuration must be dict")
            ret = False

    if ret:
        for i in SOCKET_KEYS:
            if not i in socket:
                logging.error(
                    "configuration: domain config requires `{}' key".format(
                        i
                        )
                    )
                ret = False

        for i in list(socket.keys()):
            if not i in SOCKET_KEYS and not i in SOCKET_KEYS_OPT:
                logging.error(
                    "configuration: unknown "
                    "key (`{}') found in socket config".format(
                        i
                        )
                    )
                ret = False

        if 'SSL' in socket:
            if not _correctness_check_SSL(data_dict, socket['SSL']):
                logging.error(
                    "configuration: incorrect SSL config: `{}'".format(
                        socket['SSL']
                        )
                    )
                ret = False

    # NOTE and TODO: here most likely mest be more checks

    return ret


def _correctness_check_SSL(data_dict, ssl):

    ret = True

    if ret:
        if not isinstance(ssl, dict):
            logging.error("configuration: ssl configuration must be dict")
            ret = False

    if ret:
        for i in SSL_KEYS:
            if not i in ssl:
                logging.error(
                    "configuration: ssl config requires `{}' key".format(
                        i
                        )
                    )
                ret = False

        for i in list(ssl.keys()):
            if not i in SSL_KEYS and not i in SSL_KEYS_OPT:
                logging.error(
                    "configuration: unknown "
                    "key (`{}') found in ssl config".format(
                        i
                        )
                    )
                ret = False

    # NOTE and TODO: here most likely mest be more checks

    return ret


def correctness_check(data_dict):
    """
    result: True - Ok, False - Error
    """

    ret = True

    if ret:
        if not isinstance(data_dict, dict):
            logging.error("configuration: input data must be dict")
            ret = False

    if ret:

        for i in ['domains', 'sockets']:
            if not i in data_dict:
                logging.error(
                    "configuration: input data dict must have `{}' key".format(
                        i
                        )
                    )
                ret = False
                break

    if ret:
        for each in data_dict['domains']:
            if not _correctness_check_domain(data_dict, each):
                logging.error(
                    "configuration: incorrect domain config: `{}'".format(
                        each
                        )
                    )
                ret = False
                break

        for each in data_dict['sockets']:
            if not _correctness_check_socket(data_dict, each):
                logging.error(
                    "configuration: incorrect socket config: `{}'".format(
                        each
                        )
                    )
                ret = False
                break

    return ret
