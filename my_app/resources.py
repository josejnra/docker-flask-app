import importlib

from flask import request
from flask_restful import Resource


class AbstractResource(Resource):
    """
        Abstract class to create resources.
    """
    @property
    def service_module(self):
        """
            String for the service's module path.
        """
        raise NotImplementedError

    @property
    def service_class(self):
        """
            String for the service's class name.
        """
        raise NotImplementedError

    def _get_service(self):
        """
            Method to return an instance of the service's model.

            Returns
            ----------
            Object
                An instance of the service specified in the attribute 'service_class'.
        """
        service_class = getattr(importlib.import_module(self.service_module), self.service_class)
        return service_class()

    def get(self, id_=None):
        """
            Generic method to handle a HTTP GET request.

            Parameters
            ----------
            id_: int, optional
                Entity identifier to be found.

            Returns
            ----------
            Object
                First entity found by the service.
        """
        return self._get_service().retrieve(id_)

    def post(self):
        """
            Generic method to handle a HTTP POST request.

            Returns
            ----------
            Object
                Entity created by the service.
        """
        return self._get_service().create()

    def put(self, id_=None):
        """
            Generic method to handle a HTTP PUT request.

            Parameters
            ----------
            id_: int
                Entity identifier to be updated.

            Returns
            ----------
            Object
                Entity updated by the service.

            Raises
            ----------
            EntityNotFound
                If the entity identifier is not informed.
        """
        if id_ is None:
            raise Exception('Cannot find entity without an identifier.')
        else:
            return self._get_service().update(id_)

    def delete(self, id_=None):
        """
            Generic method to handle a HTTP DELETE request.

            Parameters
            ----------
            id_: int
                Entity identifier to be deleted.

            Returns
            ----------
            Object
                Entity deleted by the service.

            Raises
            ----------
            EntityNotFound
                If the entity identifier is not informed.
        """
        if id_ is None:
            raise Exception('Cannot find entity without an identifier.')
        else:
            return self._get_service().delete(id_)

    def _get_headers_request(self):
        """
            Returns
            ----------
            dict
               Request header as a dict.

       """
        return request.headers


class TeamsResource(AbstractResource):
    service_module = 'my_app.services'
    service_class = 'TeamsService'


class PlayersResource(AbstractResource):
    service_module = 'my_app.services'
    service_class = 'PlayersService'
