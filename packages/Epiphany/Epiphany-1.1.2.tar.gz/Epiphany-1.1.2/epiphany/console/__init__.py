from epiphany.console.kernel import ConsoleApplicationKernel


class EpiphanyConsoleApplication(ConsoleApplicationKernel):
    pass


def start_epiphany():
    epiphany = EpiphanyConsoleApplication('Epiphany', 'v1.1.0')
    return epiphany.start()
