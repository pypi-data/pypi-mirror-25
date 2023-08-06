from epiphany.console.kernel import ConsoleApplicationKernel


class EpiphanyConsoleApplication(ConsoleApplicationKernel):
    pass


if __name__ == '__main__':
    epiphany = EpiphanyConsoleApplication()
    epiphany.start()
