class Prompt(object):
    """docstring for Prompt"""

    def __init__(self, pstr="> "):
        self.pstr = pstr
        self.commands = {}
        self.aliases = {}
        self.registerCommand("help", self.cmd_help, ["?"], "Print help")
        self.registerCommand("exit", self.cmd_exit, [
                             "quit"], "Exit the prompt")

    def cmd_exit(self, *args):
        raise KeyboardInterrupt

    def cmd_help(self, *args):
        for ck in self.commands:
            c = self.commands.get(ck)
            print(c.name, c.aliases, c.helpstr, sep="\t")

    def registerCommand(self, name, callback, aliases=[], helpstr=None):
        self.registerCommandObj(Command(name, callback, aliases, helpstr))

    def registerCommandObj(self, command):
        name = command.name
        self.commands[name] = command
        for a in command.aliases:
            self.aliases[a] = self.commands[name]

    def run(self):
        try:
            while True:
                inp = input(self.pstr).split(" ")
                name = inp[0]
                match = self.commands.get(name) or self.aliases.get(name)
                if match:
                    match(*inp[1:])
                else:
                    print("ERROR: No such command " + name)
        except KeyboardInterrupt as e:
            print()

    def __call__(self):
        return self.run()


class Command(object):
    """docstring for Command"""

    def __init__(self, name, callback, aliases=[], helpstr=None):
        self.name = name
        self.callback = callback
        self.aliases = aliases
        if helpstr is None:
            helpstr = "Run command {name}".format(**locals())
        self.helpstr = helpstr

    def run(self, *args):
        return self.__call__(*args)

    def __call__(self, *args):
        try:
            self.callback(*args)
        except Exception as e:
            import traceback
            traceback.print_exc()


def test():
    def echo(*args):
        print(*args)

    p = Prompt()
    p.registerCommand("echo", echo, ['print'], "Repeat input")

    p()


class Interactable(object):

    def prompt(self):
        p = Prompt()
        for name in dir(self):
            if name[0:4] == "cmd_" and hasattr(self.__getattribute__(name), '__call__'):
                p.registerCommand(name[4:], self.__getattribute__(name))
        p()

    def __init__(self):
        super().__init__()
        self.prompt()


if __name__ == "__main__":
    test()
