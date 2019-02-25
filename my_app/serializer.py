from datetime import datetime
import json

from sqlalchemy.orm.state import InstanceState


class Serializer:
    """
        Class responsible to provide serializer methods to display any object.
    """

    @staticmethod
    def json_serialize(element):
        """
            Method to serializer any element by its type to be placed in a JSON object.

            Parameters
            ----------
            element: any
                Element to be serialized.

            Raises
            ----------
            TypeNotIdentified
                If the element type cannot be identified during the serialization process.
        """
        if type(element) is str:
            return element
        if type(element) is dict:
            return json.dumps(element, indent=4, sort_keys=True, default=str)
        elif type(element) is int:
            return element
        elif type(element) is bool:
            return element
        elif element is None:
            return element
        elif type(element) is datetime:
            return datetime.isoformat(element)
        elif type(element) is InstanceState:
            return None
        else:
            raise Exception('Cannot identify type: ' + str(type(element)))
