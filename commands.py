import logging
import sys
import re
from utils.base_model import get_model_class, BaseModel


class Command:
    """Definition of syntax to call a function.
    """

    def __init__(self, syntax: str, fn: callable):
        self.syntax = syntax
        self.fn = fn
        self.pattern = self._parse_pattern(syntax)

    @staticmethod
    def _parse_pattern(syntax: str):
        ret_val = re.escape(syntax)
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


@register_command("create :model")
def create(model: str):
    class_ = get_model_class(model)
    if class_:
        table = _storage.data.get(model, [])
        new_object = class_.create()
        print("Create new object: ", new_object)
        table.append(new_object.to_dict())
        _storage.data[model] = table
        _storage.save()


@register_command("update :id_ set :field = :value")
def update(id_, field, value):
    pass


@register_command("delete :id_")
def delete(id_):
    pass


@register_command("select * from :model")
def select_all(model: str):
    table = _storage.data.get(model)
    print_basic_table(table)


def print_basic_table(data: list[dict[str, any]]):
    def f(x): return str(x)[:13].ljust(13)
    if data:
        keys = data[0].keys()
        print(" " + " | ".join(map(f, keys)))
        print("-" + " + ".join(f("-"*13) for _ in keys))
        print("\n".join(" " + " | ".join(
            map(f, (row[key] for key in keys))) for row in data))


@register_command("select :id_")
def select_one(id_: str):
    pass


@register_command("list models")
def list_models():
    print("Available models:")
    for subclass in BaseModel.__subclasses__():
        print("  " + subclass.__name__)
    print()


@register_command("describe :model")
def describe(model: str):
    class_ = get_model_class(model)
    if class_ is None:
        logging.warning(f"Invalid object type: '{model}'")
        return
    print(f"{model}:")
    for name, field in class_._get_fields().items():
        print(f"  {name}: {field.type_.__name__}")
    print()


@register_command("help")
def help_():
    print("Available commands:")
    for command in _commands:
        print(" ", re.sub(r"_$|_(\W)", r"\1", command.syntax))
    print()


@register_command("quit")
def quit_():
    sys.exit(0)
