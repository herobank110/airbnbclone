import sys
from models.engines.file_storage import FileStorage
from models.utils.base_model import get_model_class


_file_storage = FileStorage("data.json")


def create(object_type: str):
    class_ = get_model_class(object_type)
    if class_:
        table = _file_storage.data.get(object_type, [])
        new_object = class_.create()
        print("Create new object: ", new_object)
        table.append(new_object.to_dict())
        _file_storage.data[object_type] = table
        _file_storage.save()


def update():
    pass


def delete():
    pass


def select_all(object_type: str):
    table = _file_storage.data.get(object_type)
    print(table)


def select_one(object_type: str, id: str):
    table = _file_storage.data.get(object_type)


def quit_():
    sys.exit(0)