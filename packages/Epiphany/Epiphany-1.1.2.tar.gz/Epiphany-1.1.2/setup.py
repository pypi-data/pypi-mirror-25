from distutils.core import setup


setup(
    name='Epiphany',
    version='1.1.2',
    packages=['epiphany', 'epiphany.collections', 'epiphany.console', 'epiphany.support','epiphany.http'],
    entry_points={
        'console_scripts': [
            'epiphany = epiphany.console:start_epiphany'
        ]
    },
    url='http://br0kenb1nary.github.io/epiphany',
    license='MIT',
    author='Damien Rose',
    author_email='br0kenb1nary@users.noreply.github.com',
    description='Epiphany'
)
