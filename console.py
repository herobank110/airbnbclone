import re
import cmds


class Command:
    def __init__(self, syntax: str, command: callable):
        self.syntax = syntax
        self.command = command
        self.pattern = self._parse_syntax(syntax)

    @staticmethod
    def _parse_syntax(syntax: str):
        ret_val = syntax
        for match in re.findall("(:\w+)", syntax):
            ret_val = ret_val.replace(match, f"(?P<{match[1:]}>\w+)")
        return re.compile(ret_val)


commands = [Command("create :object_type", cmds.create),
            Command("update :id set :field = :value", cmds.update),
            Command("delete :id", cmds.delete),
            Command("select :id", cmds.select_one),
            Command("select * from :object_type", cmds.select_all),
            Command("quit", cmds.quit_)]


def process_line(line: str):
    """Parse and execute the line
    """

    for command in commands:
        match = command.pattern.match(line)
        if match:
            values = match.groupdict()
            command.command(**values)
            return


def run_console():
    while True:
        line = input("(hbnb) ")
        print(process_line(line))


if __name__ == "__main__":
    run_console()
