from epiphany.console.kernel import ConsoleApplicationKernel


class EpiphanyConsoleApplication(ConsoleApplicationKernel):
    pass


def start_epiphany():
    epiphany = EpiphanyConsoleApplication('Epiphany','v1.0.9')
    return epiphany.start()


if __name__ == '__main__':
    start_epiphany()
