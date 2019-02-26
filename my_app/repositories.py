import datetime
import json
import re
from abc import ABC, abstractmethod

from sqlalchemy.exc import IntegrityError
from sqlalchemy.inspection import inspect

from my_app.models import db


class AbstractRepository(ABC):
    """
        Abstract class to create repositories.
    """

    @property
    @abstractmethod
    def model_class(self):
        """
            String for the model's class name.
        """
        raise NotImplementedError

    def get_model_columns(self):
        """
            Method to return a list with the columns of the repository's model.

            Returns
            ----------
            list
                String list with the repository's model columns.
        """
        return [m.key for m in self.model_class.__table__.columns]

    def commit(self):
        return db.session.commit()

    def rollback(self):
        return db.session.rollback()

    def find(self, id_):
        """
            Generic method to find the first entity of the repository's model according to the id.

            Parameters
            ----------
            id_: int
                Entity id for its primary key.

            Returns
            ----------
            Object
                First entity of the repository's model found with the id.

            Raises
            ----------
            EntityNotFound
                If cannot be find an entity with the informed id.
        """
        primary_key = inspect(self.model_class.__class__).primary_key[0]
        entity = self.model_class.query.filter(primary_key == id_).first()

        if not entity:
            raise Exception('Entity not found!')

        return entity.to_json()

    def all(self):
        """
            Generic method to retrieve all entities of the repository's model.

            Returns
            ----------
            Object
                First entity of the repository's model found with the id.
        """
        array = [entry.to_json() for entry in self.model_class.query.all()]
        return array

    def create(self, args, commit_at_the_end=True):
        """
            Generic method to persist an entity of the repository's model.

            Parameters
            ----------
            args: list
                Entity's values to be persisted.

            commit_at_the_end: boolean
                Flag to automatically execute the db.session.commit() after insert the model and no error occurs.

            Returns
            ----------
            Object
                Entity after be persisted.

            EntityAlreadyExists
                If an integrity error is identified during the create process.
        """
        new_model = self.model_class
        for key, value in args.items():
            pattern = '\.'+key+'$'
            for attribute in new_model.__table__.columns:
                if re.search(pattern, str(attribute)):
                    setattr(new_model, key, value)
        try:
            db.session.add(new_model)
            db.session.flush()
        except IntegrityError as exp1:
            db.session.rollback()
            raise Exception('Entity already exists. Integrity_error' + json.dumps(exp1.orig.args))
        except Exception as exp2:
            db.session.rollback()
            raise exp2
        else:
            if commit_at_the_end:
                db.session.commit()
            return new_model.to_json()

    def update(self, id_, args, commit_at_the_end=True):
        """
            Generic method to update an entity of the repository's model.

            Parameters
            ----------
            id_: int
                Entity's identifier that needs to be updated.

            args: list
                Entity's values to be update.

            commit_at_the_end: boolean
                Flag to automatically execute the db.session.commit() after insert the model and no error occurs.

            Returns
            ----------
            Object
                Entity after be updated.

            Raises
            ----------
            EntityNotFound
                If cannot be find an entity with the informed id.

            EntityAlreadyExists
                If an integrity error is identified during the update process.
        """
        primary_key = inspect(self.model_class.__class__).primary_key[0]
        model = self.model_class.query.filter(primary_key == id_).first()
        if not model:
            raise Exception('Cannot find entity')
        for key, value in args.items():
            for attribute in model.to_dict().keys():
                if key == attribute:
                    setattr(model, key, value)
                elif key == 'updated_at':
                    setattr(model, key, datetime.datetime.utcnow())
        try:
            db.session.flush()
        except IntegrityError as exp1:
            db.session.rollback()
            raise Exception('Entity cannot be updated. Integrity_error' + json.dumps(exp1.orig.args))
        except Exception as exp2:
            db.session.rollback()
            raise exp2
        else:
            if commit_at_the_end:
                db.session.commit()
            return model.to_json()

    def delete(self, id_):
        """
           Generic method to delete an entity of the repository's model.

           Parameters
           ----------
           id_: int
               Entity's identifier that needs to be deleted.

           Returns
           ----------
           Object
               Object with a success message after the entity is deleted.

           Raises
           ----------
           EntityNotFound
               If cannot be find an entity with the informed id.
       """
        primary_key = inspect(self.model_class.__class__).primary_key[0]
        model = self.model_class.query.filter(primary_key == id_).first()
        if not model:
            raise Exception('Cannot find entity')
        db.session.delete(model)
        db.session.commit()
        return {'message': 'Entity deleted successfully'}


class TeamsRepository(AbstractRepository):

    from my_app.models import TeamsModel

    model_class = TeamsModel()


class PlayersRepository(AbstractRepository):

    from my_app.models import PlayersModel

    model_class = PlayersModel()
