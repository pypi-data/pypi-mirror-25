from django.conf.urls import url

from rinzler.core.router import Router


class UrlAssembler(object):

    auth_service = None
    base_path = str()
    logger = object

    def mount(self, route, callback):
        """
        Mounts a route with the given params
        :rtype: urls
        """
        return url(
            r'{0}'.format(route),
            Router(route, callback).register('log', self.logger).auth_config(self.auth_service).route
        )

    def set_auth_service(self, auth_service):
        """
        Sets the authentication service
        :rtype: object
        """
        self.auth_service = auth_service
        return self

    def set_logger(self, logger: object()):
        self.logger = logger
        return self
