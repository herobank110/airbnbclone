import logging
import sys
import re
from utils.base_model import get_model_class


class Command:
    """Definition of syntax to call a function.
    """

    def __init__(self, syntax: str, fn: callable):
        self.syntax = syntax
        self.fn = fn
        self.pattern = self._parse_pattern(syntax)

    @staticmethod
    def _parse_pattern(syntax: str):
        ret_val = syntax
        for match in re.findall("(:\w+)", syntax):
            ret_val = ret_val.replace(match, f"(?P<{match[1:]}>\w+)")
        return re.compile(ret_val)


_commands: list[Command] = []


def register_command(syntax: str):
    """Decorator for functions that may be executed from the console.
    :param syntax: the command syntax. May include parameters by starting
    a word with colon that will be passed to the function when called.
    Eg, 'my_command :param1 :param2'
    """
    def command_inner(fn):
        _commands.append(Command(syntax, fn))
        return fn
    return command_inner


def process_line(storage, line: str):
    """Parse and execute the line
    """
    global _storage
    _storage = storage

    for command in _commands:
        match = command.pattern.match(line)
        if match:
            values = match.groupdict()
            command.fn(**values)
            return
    logging.warning("No matching command found")

# Register Commands


@register_command("create :object_type")
def create(object_type: str):
    class_ = get_model_class(object_type)
    if class_:
        table = _storage.data.get(object_type, [])
        new_object = class_.create()
        print("Create new object: ", new_object)
        table.append(new_object.to_dict())
        _storage.data[object_type] = table
        _storage.save()


@register_command("update :id_ set :field = :value")
def update(id_, field, value):
    pass


@register_command("delete :id_")
def delete(id_):
    pass


@register_command("select * from :object_type")
def select_all(object_type: str):
    table = _storage.data.get(object_type)
    print(table)


@register_command("select :id_")
def select_one(id_: str):
    pass
    # table = _file_storage.data.get(object_type)


@register_command("quit")
def quit_():
    sys.exit(0)
