from abc import abstractmethod

from flask_restful import Resource

from my_app.services import TeamsService, PlayersService


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
    @abstractmethod
    def service_class(self):
        """
            String for the service's class name.
        """
        raise NotImplementedError

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
        return self.service_class.retrieve(id_)

    def post(self):
        """
            Generic method to handle a HTTP POST request.

            Returns
            ----------
            Object
                Entity created by the service.
        """
        return self.service_class.create()

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
            return self.service_class.update(id_)

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
            return self.service_class.delete(id_)


class TeamsResource(AbstractResource):

    service_class = TeamsService()


class PlayersResource(AbstractResource):

    service_class = PlayersService()
