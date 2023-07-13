from utils.commands import process_line
from models.engines.file_storage import FileStorage
import logging
logging.basicConfig(format="%(levelname)s: %(message)s")


def run_console():
    storage = FileStorage("data.json")
    print("Welcome to hbnb console\n"
          "\n"
          "To view all commands, enter 'help'\n")
    while True:
        line = input("(hbnb) ")
        process_line(storage, line)


if __name__ == "__main__":
    run_console()
