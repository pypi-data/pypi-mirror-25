import inspect
from inspect import _empty
from salar.sugar import *
from salar.webapi import HttpError


def get_adaptors(func, cls):
    """
    >>> from salar.cli import CliParam
    >>> @_annotate(bob=CliParam(vartype=int, short='b', long='bob', default=1))
    ... def show(alice:int=4, bob=8):
    ...     ' :param bob: Bob'
    ...     return alice + bob
    >>> adaptors = get_adaptors(show, CliParam)
    >>> assert list(adaptors.keys()) == ['alice', 'bob']
    >>> assert adaptors['alice'].__dict__ == dict(vartype=int, short='', long='', slot='', default=4, doc='')
    >>> assert adaptors['bob'].__dict__ == dict(vartype=int, short='b', long='bob', slot='', default=8, doc='Bob')
    """
    lines = func.__doc__.splitlines()
    doc_dict = {}
    for line in map(str.strip, lines):
        if line.startswith(':param '):
            key, value = map(str.strip, line.split(':param ', 1)[-1].split(':', 1))
            doc_dict[key] = value
    adaptors = {}
    for name, _, _ in get_func_parameters(func):
        adaptors[name] = cls()
    for name, anno in get_annotations(func).items():
        h, name = name[0], name[1:]
        if h == '@' and name:
            adaptors[name] = anno
    for name, vartype, default in get_func_parameters(func):
        adaptor = adaptors.setdefault(name, cls())
        if vartype is not _nil:
            adaptor.vartype = vartype
        if default is not _nil:
            adaptor.default = default
        if name in doc_dict:
            adaptor.doc = doc_dict[name]
    return adaptors


def get_func_parameters(func):
    """
    >>> def f(a:int, b=4)->int:
    ...   return a+b
    >>> ret = get_func_parameters(f)
    >>> assert ret == [('a', int, _nil), ('b', _nil, 4)]
    """
    return [
        (
            p,
            _nil if q.annotation is _empty else q.annotation ,
            _nil if q.default is _empty else q.default,
        )
        for p, q in inspect.signature(func).parameters.items()
    ]


def get_annotations(x):
    try:
        annotations = x.__annotations__
    except:
        annotations = {}
    return annotations


def fields_doc(fn):
    annotations = get_annotations(fn)
    params = {}
    #for k, v in annotations.items():
    #    if k == 'result': continue
    #    params[k] = dict(
    #        vartype=str(v.vartype).split('\'')[1],
    #        source=v.source.name,
    #        default=v.default,
    #        doc=v.doc,
    #    )
    return dict(params=params, doc=fn.__doc__ or '')


html_tpl = """<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="utf-8">
    <title>ApiDoc</title>
</head>
<body>
{}
</body>
</html>
"""

def mapping_list_doc(mappings, prefix):
    rows = []
    for mapping in mappings:
        if mapping.pattern.startswith(prefix): continue
        item = dict(
            pattern=mapping.pattern,
            method=mapping.method,
            fname=mapping.fn.__name__,
            doc=mapping.doc,
        )
        rows.append("""<div>
            pattern: {pattern} | method: {method} | name: <a href="api_{fname}.html">{fname}</a> | doc: {doc}
            </div>
            """.format(**item))

    body_tpl = ''.join(rows)
    return html_tpl.format(body_tpl)


def controller_detail_doc(mappings, fname):
    _ = [x.fn for x in mappings if x.fn.__name__ == fname]
    if not _:
        raise HttpError(status_code=404, text='Not Found', headers={})
    fn = _[0]
    doc_stack = _eafp(lambda: fn.doc_stack[-1], fields_doc(fn))
    params, doc = doc_stack['params'], doc_stack['doc']
    params_tpl = ''.join("""<div>field: {name} | type: {vartype} | source: {source} | default: {default} | doc: {doc}</div>\n""".format(name=k, **v) for k, v in params.items())
    body_tpl = """{} <hr/> 说明：<br/><tt><pre>{}</pre></tt>""".format(params_tpl, doc)
    return html_tpl.format(body_tpl)
