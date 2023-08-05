import os

from salar import cli
from salar.cli import CliParam, Restrict
from salar.sugar import _annotate


sample_text = '''___
$ {name} -c --output out main.c -n 10
FOO OK
$ {name} copy -f a.txt
COPY OK
___
from salar import cli
from salar.cli import Argument, Restrict

def foo(
        name: Argument(slot='file', doc='input file'),
        is_compile: Argument(vartype=bool, short='c', long='compile', default=False, doc='compile'),
        output: Argument(short='o', long='output', slot='file', doc='output file'),
        number: Argument(vartype=int, short='n', slot='num', default=0, doc='set a number')
):
    ___
    {name} [OPTIONS] <in-file>             Usage of foo.
    ___
    print(name, is_compile, output, number)
    print('FOO OK')

def copy(
        file: Argument(short='f', slot='file', doc='input file')
):
    ___
    {name} copy [OPTIONS] ...              Usage of copy.
    ___
    try:
        cli.copy(open(file).read())
        print('COPY OK')
    except:
        raise cli.error('-f <file> : file not exist OR copy() not supported by os')

def main():
    overview = "This is overview of {name}"
    cli.Cli(overview).add('', foo).add('copy', copy, Restrict.ONLY_ONE).run()

if __name__ == '__main__':
    main()
'''

setup_text = '''from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path
import subprocess
from setuptools.command.install import install

here = path.abspath(path.dirname(__file__))

class MyInstall(install):
    def run(self):
        print("-- installing... (powered by salar) --")
        install.run(self)

setup(
        name = '{name}',
        version='0.0.1',
        description='',
        long_description='',
        url='',
        author='',
        author_email='',
        license='MIT',
        platforms=['any'],

        classifiers=[
            ],
        keywords='{name}',
        packages = ['{name}'],
        install_requires=['salar>=0.0.1'],

        cmdclass={'install': MyInstall},
        entry_points={
            'console_scripts': [
                '{name} = {name}.run:main',
                ],
            },
    )
'''


@_annotate(name=CliParam(slot='name', doc='tool name'))
def create(name):
    """
    salar create <name>       : Create template of CLI tool
    """
    os.mkdir(name)
    os.mkdir('{name}/{name}'.format(name=name))
    with open('{name}/{name}/__init__.py'.format(name=name), 'w') as f:
        f.write('')
    with open(name + '/setup.py', 'w') as f:
        f.write(setup_text.replace('{name}', name))
    with open('{name}/{name}/run.py'.format(name=name), 'w') as f:
        tpl = sample_text.replace('{name}', name).replace('___', '\"\"\"')
        f.write(tpl)
    print('-- OK --')
    print('please edit {name}/{name}/run.py for your need\n'.format(name=name))


@_annotate(name=CliParam(slot='name', doc='tool name'))
def install(name):
    """
    salar install <name>      : Install CLI tool
    """
    cmd = 'cd {}; python setup.py install'.format(name)
    print(cmd)
    os.system(cmd)


@_annotate(name=CliParam(slot='name', doc='tool name'))
def uninstall(name):
    """
    salar uninstall <name>    : Uninstall CLI tool
    """
    cmd = 'python -m pip uninstall ' + name
    print(cmd)
    os.system(cmd)


def submit():
    """
    salar submit              : Submit your tool to pypi.python.org
    """
    text = 'Please edit your own ~/.pypirc and setup.py, and then run this command below:\n' + \
           '  cd <name>; python setup.py bdist_wheel upload\n'
    print(text)


def hello(port: int):
    """
    :param port: server port
    salar hello
    """
    from aiohttp import web
    from aiohttp_wsgi import WSGIHandler
    from salar import application
    app = application()
    app.add_mapping(pattern='/', method='GET', fn=lambda ctx: 'Hello salar (3)')
    httpd = web.Application()
    httpd.router.add_route("*", "/{path_info:.*}", WSGIHandler(app.wsgifunc()))
    web.run_app(httpd, port=port)


def main():
    overview = "Tookit for generating command line interfaces"
    app = cli.Cli(overview)
    app.add("create", create, Restrict.NOT_EMPTY)
    app.add("install", install, Restrict.NOT_EMPTY)
    app.add("uninstall", uninstall, Restrict.NOT_EMPTY)
    app.add("submit", submit)
    app.add("hello", hello)
    app.run()
