import subprocess

from termcolor import cprint


class ConsoleApplicationKernelManifest(type):
    extension_bindings = {
        'js' : 'node',
        'php': 'php',
        'py' : 'python'
    }


class ConsoleApplication:
    """
    This module exports the following functions:
        start           Starts the console
        execute         Allows for execution of external applications or scripts
    """
    configuration = {'app_name': None, 'app_version': None}

    # TODO : Color on color
    notifications = {'success': 'green', 'info': 'blue', 'warn': 'yellow', 'error': 'red'}

    processes = {}

    running = False

    command = property(lambda self: self.response.get('cmd'))
    arguments = property(lambda self: self.response.get('args'))


    @property
    def response(self):
        return self.__response__


    @response.setter
    def response(self, line):
        self.__response__ = {'cmd': line[0] if line is not None else [], 'args': line[1:] if line is not None else []}


    def __init__(self, app_name='', app_version=None):
        """ Instantiates the console application, defining the application name
            as well as the application version prior to prompting for input """
        self.configuration.update({'app_name': app_name})
        self.configuration.update({'app_version': app_version})


    def help(self):
        # TODO: Define help command
        print("Nothing here yet")


    def __stdin__(self):
        """ Requests the users input via the command line console by prompting the
            name of the application in lower case as defined upon instantiation"""
        return input('%s> ' % self.configuration.get('app_name').lower()).split()


    def __valid__(self):
        """ Determines whether or not the command entered is defined as
            a valid callback within the Console class, returning accordingly"""
        if hasattr(self, getattr(self, 'command')):
            return getattr(self, getattr(self, 'command'))

        # Commented out until I can find a fix for windows ASCII character resolution
        # self.writer.warning('No command exists for %s' % getattr(self,'command') )
        return False


    def execute(self, command, *args):
        """ Executes an a process and returns the responses """
        response = subprocess.run([command, *args], stdout=subprocess.PIPE, shell=True)
        return {'response': response.returncode, 'error': response.stderr, 'verbose': str(response.stdout, 'utf-8')}


    def quit(self):
        """ Terminates the current console session with a hard exit """
        exit(0)


    def run(self, file):
        # TODO: Bindings
        pass


    def notification(self, message, type='success'):
        cprint(message, self.notifications[type])


    def start(self):
        """ Instantiates a new terminal session """
        self.running = True
        while self.running:
            self.response = self.__stdin__()
            request = self.__valid__()
            if self.__valid__():
                request(*iter(self.arguments))
