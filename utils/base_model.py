from datetime import datetime
import uuid
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

    id_ = Field(uuid.UUID)

    def __init__(self, **kwargs):
        """Set fields by kwargs, with validation for data types.
        """
        for key, value in kwargs.items():
            field = getattr(self, key, None)
            if field is None:
                logging.warning(
                    f"Unexpected key for initializing model: {key}")
                continue
            if not isinstance(field, Field):
                logging.warning(
                    f"Invalid key type for initializing model: {key}")
                continue
            if value is not None and type(value) is not field.type_:
                logging.warning(
                    f"Invalid value type for initializing model: {value}")
                continue
            field.value = value

    @classmethod
    def create(cls):
        return cls(id_=uuid.uuid4())
        # obj.created_at = datetime.now()
        # obj.updated_at = datetime.now()
        return obj

    @classmethod
    def load(cls, json_obj: dict):
        for key, value in json_obj.items():
            obj = cls()

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
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, uuid.UUID):
        return value.hex
    return value


def deserialize(type_: Type[FieldValueType], json_value) -> FieldValueType:
    # Primitive types will be converted to python types already.
    if json_value:
        # value is not null or empty
        if type_ is uuid.UUID:
            return uuid.UUID(json_value)
        if type_ is datetime:
            date_format = '%Y-%m-%dT%H:%M:%S.%f'
            return datetime.strptime(json_value, date_format)


def get_model_class(object_type: str) -> BaseModel:
    class_ = next((subclass for subclass in BaseModel.__subclasses__()
                   if subclass.__name__ == object_type), None)
    if class_ is None:
        logging.warning(f"Couldn't find model class for type '{object_type}'")
    return class_
