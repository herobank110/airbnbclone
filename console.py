import cmds


def run_console():
    while True:
        line = input("(hbnb) ")
        cmds.process_line(line)


if __name__ == "__main__":
    run_console()
