import xmlrpclib


class SupervisorClient:
    # supervisor didn't supply some "restart"  xmlrpc
    # these extra is to wrap them with "stop" and "start"
    extra_methods = ['restart_process', 'restart_process_group']

    def __init__(self, ip, port, username=None, password=None):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

        if username and password:
            self.uri = 'http://%s:%s@%s:%s/RPC2' % (
                username, password, ip, port
            )
        else:
            self.uri = 'http://%s:%s/RPC2' % (ip, port)

        self.supervisor = xmlrpclib.Server(self.uri).supervisor

    def call(self, method, *params):
        """
        call xmlrpc

        :param method:
        :param params:
        :return:
        """
        if method in SupervisorClient.extra_methods:
            return getattr(self, method)(*params)
        else:
            return getattr(self.supervisor, method)(*params)

    def restart_process(self, name):
        """
        stop and start process through xmlrpc

        :param name:
        :return:
        """
        process_info = getattr(self.supervisor, 'getProcessInfo')(name)

        if process_info['statename'] == 'RUNNING':
            getattr(self.supervisor, 'stopProcess')(name)

        return getattr(self.supervisor, 'startProcess')(name)

    def restart_process_group(self, group):
        """
        stop and start process group through xmlrpc

        :param group:
        :return:
        """
        getattr(self.supervisor, 'stopProcessGroup')(group)
        return getattr(self.supervisor, 'startProcessGroup')(group)
