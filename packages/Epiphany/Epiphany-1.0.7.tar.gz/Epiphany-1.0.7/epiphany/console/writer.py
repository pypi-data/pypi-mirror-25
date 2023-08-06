from termcolor import colored
class ConsoleApplicationWriterManifest(type):
    def __call__(self, *args, **kwargs):
        print(args)

    def __getattr__(self, item):
        return callable([self,item])

class ConsoleApplicationWriter(metaclass=ConsoleApplicationWriterManifest):
    pass