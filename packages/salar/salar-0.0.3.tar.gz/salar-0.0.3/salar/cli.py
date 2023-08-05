from typing import Any
import sys
from enum import Enum
from salar.apidoc import get_adaptors


class Restrict(Enum):
    NO_RESTRICT = 0
    NOT_EMPTY = 1
    ONLY_ONE = 2
    ALL = 3


class CliParam(object):
    def __init__(self, vartype:Any=None, short:str='', long:str='', slot:str='', default:Any=None, doc:str=''):
        self.vartype = vartype
        self.short = short
        self.long = long
        self.slot = slot
        self.default = default
        self.doc = doc


def extract_args(arg_list, annotations, restrict):
    result = {k: p.default for k, p in annotations}
    i = 0
    key_count = 0
    try:
        while i < len(arg_list):
            raw_arg = arg_list[i]
            if raw_arg[0] == '-':
                index, key, prop = [(i, k, p) for i, (k, p) in enumerate(annotations)
                                    if '-' + p.short == raw_arg or '--' + p.long == raw_arg][0]
            else:
                index, key, prop = [(i, k, p) for i , (k, p) in enumerate(annotations)
                                    if not p.short and not p.long][0]
            annotations.pop(index)
            if prop.vartype is bool:
                result[key] = True; i += 1
            elif prop.vartype is str or prop.vartype is int:
                if raw_arg[0] == '-':
                    result[key] = prop.vartype(arg_list[i + 1]); i += 2
                else:
                    result[key] = prop.vartype(arg_list[i]); i += 1
            else:
                raise NotImplementedError
            key_count += 1
    except IndexError:
        raise help()
    except Exception as e:
        raise error(str(e))
    if (restrict == Restrict.NOT_EMPTY and key_count == 0) or \
            (restrict == Restrict.ONLY_ONE and key_count != 1) or \
            (restrict == Restrict.ALL and key_count != len(annotations)):
        raise help()
    return result


def update_adaptors(adaptors):
    for name, adaptor in adaptors.items():
        if not any((adaptor.short, adaptor.long, adaptor.slot)):
            adaptor.short = name[0]
            adaptor.long = name
        if adaptor.vartype is bool:
            adaptor.slot = ''
        elif not adaptor.slot:
            adaptor.slot = name
        if not adaptor.vartype:
            adaptor.vartype = str
    return adaptors


class Cli(object):
    def __init__(self, overview):
        self.overview = overview
        self.workers = []

    def add(self, path, worker, restrict=Restrict.NO_RESTRICT):
        """
        >>> cli = Cli('test')
        >>> є = Restrict
        >>> cli = cli.add('hello', str.strip, є.NO_RESTRICT)
        >>> cli = cli.add('hi there', str.split, є.ALL)
        >>> assert cli.workers[0] == (('hello',), str.strip, є.NO_RESTRICT)
        >>> assert cli.workers[1] == (('hi', 'there'), str.split, є.ALL)
        """
        assert isinstance(path, str), path
        assert isinstance(restrict, Restrict)
        segs = tuple(path.split()) if path.strip() else tuple()
        self.workers.append((segs, worker, restrict))
        return self

    def get_doc(self):
        lines = []
        for _, worker, _ in self.workers:
            doc = worker.__doc__
            doc = doc.strip() if doc else worker.__name__
            lines.append('  ' + doc)
            bufs = []; maxn = 0
            for _, prop in update_adaptors(get_adaptors(worker, CliParam)).items():
                buf = []
                if prop.short:
                    buf.append('-' + prop.short)
                if prop.long:
                    buf.append('--' + prop.long)
                if prop.slot:
                    buf.append('<' + prop.slot + '>')
                _ = ' '.join(buf)
                bufs.append((_, prop.doc))
                maxn = max(maxn, len(_))

            for left, doc in bufs:
                left = left.ljust(maxn + 2)
                lines.append('    ' + left + ': ' + doc)

            lines.append('')

        return '\n'.join(lines) + '\n'

    def run(self, arg_list=None):
        if arg_list is None:
            arg_list = sys.argv[1:]
        help_text = 'OVERVIEW\n  {}\n\nUSAGE\n'.format(self.overview) + \
                    self.get_doc() + \
                    '  -h --help : for more information on a command.\n'
        if len(arg_list) == 1 and arg_list[0] in ('-h', '--help'):
            print(help_text)
            return
        self.workers.sort(reverse=True)
        try:
            for suffix_tuple, worker, restrict in self.workers:
                zip_tuple = list(zip(arg_list, suffix_tuple))
                if all(x == y for x, y in zip_tuple) and len(zip_tuple) == len(suffix_tuple):
                    arg_list = arg_list[len(suffix_tuple):]
                    adaptors = update_adaptors(get_adaptors(worker, CliParam))
                    arg_dict = extract_args(arg_list, list(adaptors.items()), restrict)
                    worker(**arg_dict)
                    break

            else:
                raise help()

        except CliError as e:
            if e.is_help:
                print(help_text)
            else:
                print('error: ' + e.message)


def help():
    return CliError(True, '-h --help for help')


def error(message):
    return CliError(False, message)


def copy(text):
    import pyperclip
    pyperclip.copy(text)


def paste():
    import pyperclip
    return pyperclip.paste()


class CliError(Exception):
    def __init__(self, is_help, message):
        self.message = message
        self.is_help = is_help
