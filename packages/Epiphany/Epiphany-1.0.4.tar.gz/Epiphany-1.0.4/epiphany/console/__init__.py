from epiphany.console.kernel import ConsoleApplicationKernel


def __entrypoint__(cls):
    cls.__init__(ConsoleApplicationKernel() ,'Epiphany' ,'v1.0.3')