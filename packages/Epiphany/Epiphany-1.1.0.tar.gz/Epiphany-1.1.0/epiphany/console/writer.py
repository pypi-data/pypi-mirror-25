from termcolor import cprint


class ConsoleApplicationWriterManifest(type):
    def __call__(self, *args, **kwargs):
        print(args)


    def __getattr__(self, item):
        return callable([self, item])


class ConsoleApplicationWriter(metaclass=ConsoleApplicationWriterManifest):
    def success(self, message):
        cprint(message, 'green')


    def info(self, message):
        cprint(message, 'blue')


    def warning(self, message):
        cprint(message, 'yellow')


    def error(self, message):
        cprint(message, 'red')
