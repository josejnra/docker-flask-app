import importlib
from abc import ABC, abstractmethod

from flask_restful import reqparse
from werkzeug.exceptions import BadRequest


class AbstractService(ABC):
    """
        Abstract class to create services.
    """

    @property
    @abstractmethod
    def repository_module(self):
        """
            String for the repository's module path.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def repository_class(self):
        """
            String for the repository's class name.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def required_on_create(self):
        """
            String list of the columns that have required value to be informed for the CREATE process.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def required_on_retrieve(self):
        """
            String list of the columns that have required value to be informed for the RETRIEVE process.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def required_on_update(self):
        """
            String list of the columns that have required value to be informed for the UPDATE process.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def required_on_delete(self):
        """
            String list of the columns that have required value to be informed for the DELETE process.
        """
        raise NotImplementedError

    @property
    def ignore_on_create(self):
        """
            String list of the columns to be ignored if a value is informed inside the payload for the CREATE process.
        """
        return ['id', 'slug', 'created_at', 'updated_at']

    @property
    def ignore_on_update(self):
        """
            String list of the columns to be ignored if a value is informed inside the payload for the UPDATE process.
        """
        return ['id', 'slug', 'created_at', 'updated_at']

    def _get_repository(self):
        """
            Method to return an instance of the repository's model.

            Returns
            ----------
            Object
                An instance of the repository specified in the attribute 'repository_class'.
        """
        service_class = getattr(importlib.import_module(self.repository_module), self.repository_class)
        return service_class()

    def _validate_by_parse(self, required_list, ignore_list={}):
        """
           Method to validate the request payload.

           It will verify if the request columns were informed according to one of the request_lists (required_on_create, required_on_update, required_on_delete, required_on_list).

           Also, will clean the payload according to the ignore_lists (ignore_on_create, ignore_on_update).

           Returns
           ----------
           Object
               JSON payload after validation.

           Raises
           ----------
           MissingData
                If a required column is not informed in the payload.

           CannotBeBlank
               If a required column is informed in the payload but its value is blank.
       """
        columns = self._get_repository().get_model_columns()

        parser = reqparse.RequestParser()
        for column in columns:
            if column in required_list:
                parser.add_argument(column, required=True, nullable=False, help='Attribute \''+column+'\' cannot be find.')
            elif column not in ignore_list:
                parser.add_argument(column, required=False)

        try:
            args = parser.parse_args()
        except BadRequest as exp:
            raise Exception('Dados não foram informados corretamente.', 400, exp.data)

        for key, arg in args.items():
            if (key in required_list) and (not arg or not str(arg).strip()):
                raise Exception('Attribute \''+key+'\' cannot be blank.')

        return args

    def create(self):
        """
            Generic method to create a entity using the repository's model.

            Returns
            ----------
            Object
                New entity created by the repository's model.
        """
        args = self._validate_by_parse(self.required_on_create, self.ignore_on_create)
        return self._get_repository().create(args)

    def retrieve(self, id_):
        """
            Generic method to retrieve a entity using the repository's model.

            Parameters
            ----------
            id_: int
                Entity identifier to be retrieved.

            Returns
            ----------
            Object
                An entity found by the repository's model using the identifier.
        """
        self._validate_by_parse(self.required_on_retrieve)
        if id_ is None:
            return self._get_repository().all()
        else:
            return self._get_repository().find(id_)

    def update(self, id_):
        """
            Generic method to update an entity using the repository's model.

            Parameters
            ----------
            id_: int
                Entity identifier to be updated.

            Returns
            ----------
            Object
                The updated entity selected using the identifier by the repository's model.
        """
        args = self._validate_by_parse(self.required_on_update, self.ignore_on_update)
        return self._get_repository().update(id_, args)

    def delete(self, id_):
        """
            Generic method to delete an entity using the repository's model.

            Parameters
            ----------
            id_: int
                Entity identifier to be deleted.

            Returns
            ----------
            Object
                A message confirming the deletion by repository's model.
        """
        self._validate_by_parse(self.required_on_delete)
        return self._get_repository().delete(id_)


class TeamsService(AbstractService):

    repository_module = 'my_app.repositories'
    repository_class = 'TeamsRepository'


class PlayersService(AbstractService):

    repository_module = 'my_app.repositories'
    repository_class = 'PlayersRepository'
