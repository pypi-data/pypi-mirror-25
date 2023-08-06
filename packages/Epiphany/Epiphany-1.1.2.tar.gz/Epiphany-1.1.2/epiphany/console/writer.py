from termcolor import cprint


class ConsoleApplicationWriter:
    def success(self, message):
        cprint(message, 'green')


    def info(self, message):
        cprint(message, 'blue')


    def warning(self, message):
        cprint(message, 'yellow')


    def error(self, message):
        cprint(message, 'red')
