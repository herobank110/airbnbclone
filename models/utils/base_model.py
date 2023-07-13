from datetime import datetime
from uuid import uuid4
from datetime import datetime
from typing import Type, Union
import logging


FieldValueType = Union[str, int, float, datetime]


class Field:
    def __init__(self, type_: Type[FieldValueType]):
        self.type_ = type_
        self.value = None


class BaseModel:
    """Parent class for all models to determine saving/loading.
    """

    def __init__(self, **kwargs):
        """
        Initialize attributes: uuid4, dates when class was created/updated
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def create(cls):
        obj = cls()
        # obj.id = str(uuid4())
        # obj.created_at = datetime.now()
        # obj.updated_at = datetime.now()
        # models.storage.new(obj)
        return obj

    # def __str__(self):
    #     """
    #     Return class name, id, and the dictionary
    #     """
    #     return ('[{}] ({}) {}'.
    #             format(self.__class__.__name__, self.id, self.__dict__))

    # def __repr__(self):
    #     """
    #     returns string repr
    #     """
    #     return (self.__str__())

    # def save(self):
    #     """
    #     Instance method to:
    #     - update current datetime
    #     - invoke save() function &
    #     - save to serialized file
    #     """
    #     self.updated_at = datetime.now()
    #     models.storage.save()

    def to_dict(self):
        """
        Return dictionary of BaseModel with string formats of times
        """
        return {
            name: serialize(field.value)
            for name, field in self._get_fields().items()
        }

    def _get_fields(self):
        return {key: value
                for key, value in ((key, getattr(self, key)) for key in dir(self))
                if isinstance(value, Field)}


def serialize(value: FieldValueType):
    return str(value)


def deserialize(value_str: str) -> FieldValueType:
    return value_str
    date_format = '%Y-%m-%dT%H:%M:%S.%f'
    if "created_at" == key:
        self.created_at = datetime.strptime(kwargs["created_at"],
                                            date_format)
    elif "updated_at" == key:
        self.updated_at = datetime.strptime(kwargs["updated_at"],
                                            date_format)
    elif "__class__" == key:
        pass


def get_model_class(object_type: str) -> BaseModel:
    class_ = next((subclass for subclass in BaseModel.__subclasses__()
                   if subclass.__name__ == object_type), None)
    if class_ is None:
        logging.warning(f"Couldn't find model class for type '{object_type}'")
    return class_
