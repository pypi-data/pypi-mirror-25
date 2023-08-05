from typing import NamedTuple, Any, Callable, Optional, overload, Dict, List
import cgi
import itertools
import json
import os
import re

from io import BytesIO
from types import GeneratorType

from salar.webapi import HttpError, BadRequestError
from salar.sugar import *
from salar.apidoc import mapping_list_doc, controller_detail_doc, fields_doc, get_annotations, get_func_parameters


def _process_fieldstorage(fs):
    if isinstance(fs, list):
        return _process_fieldstorage(fs[0])
    elif fs.filename is None:
        return fs.value
    else:
        return dict(filename=fs.filename, value=fs.value)


def _dictify(fs):
    # hack to make input work with enctype='text/plain.
    if fs.list is None:
        fs.list = []
    return dict([(k, _process_fieldstorage(fs[k])) for k in fs.keys()])


@_struct
class Context(object):
    status_code: int = 200
    reason: str = 'OK'
    headers: Dict = {}
    app_stack: List = []

    url_input: Dict = {}
    json_input: Optional[Dict] = None
    _post_data: Optional[Dict] = None
    _fields: Optional[Dict] = None
    input: Dict = {}

    environ: Dict = {}
    env: Dict = {}
    host: str = ''
    protocol: str = ''
    homedomain: str = ''
    homepath: str = ''
    home: str = ''
    realhome: str = ''
    ip: str = ''
    method: str = ''
    path: str = ''
    query: str = ''
    fullpath: str = ''

    me: Any = None
    db: Any = None
    need_commit: bool = False

    def __call__(self):
        return self.app_stack[-1](self)

    def set_header(self, header, value):
        assert isinstance(header, str) and isinstance(value, str)
        if '\n' in header or '\r' in header or '\n' in value or '\r' in value:
            raise ValueError('invalid characters in header')
        self.headers[header] = value

    def get_header(self, header, default=None):
        key = 'HTTP_' + header.replace('-', '_').upper()
        return self.env.get(key, default)

    def is_json_request(self):
        return self.json_input is not None or \
               self.env.get('CONTENT_TYPE', '').lower() == 'application/json'

    @property
    def field_input(self):
        if self.json_input is not None:
            return self.json_input
        if self._fields is not None:
            return self._fields
        if self.is_json_request():
            try:
                self.json_input = json.loads(self.data().decode('utf-8'))
            except:
                self.json_input = {'__error__': 'invalid json received'}
            return self.json_input
        else:
            fp = BytesIO(self.data())
            try:
                # cgi.FieldStorage can raise exception when handle some input
                _ = cgi.FieldStorage(fp=fp, environ=self.env.copy(), keep_blank_values=1)
                self._fields = _dictify(_)
            except:
                self._fields = {'__error__': 'invalid fields received'}
        return self._fields

    def data(self):
        if self._post_data is not None:
            return self._post_data
        try:
            cl = int(self.env.get('CONTENT_LENGTH'))
        except:
            cl = 0
        self._post_data = self.env['wsgi.input'].read(cl)
        return self._post_data
    # ~class Context


class ModelView(NamedTuple):
    controller: Callable


# ctx.interceptors: List[Interceptor]
@_struct
class Interceptor:
    @overload
    def __init__(self, prefix, method, fn): pass
    prefix: str
    method: str
    fn: Callable


# ctx.mapping: List[Mapping]
@_struct
class Mapping:
    @overload
    def __init__(self, pattern, method, fn, doc, patternobj): pass
    pattern: str
    method: str
    fn: Callable
    doc: str
    patternobj: Any


# ctx.serializers: List[Serializer]
@_struct
class Serializer:
    @overload
    def __init__(self, varclass, fn): pass
    varclass: Any
    fn: Callable


class RestParam:
    def __init__(self, getter:Callable=str, jsongetter:Optional[Callable]=None, default:Any=None, queryname:Optional[str]=None, doc:str=''):
        self.getter = getter  # 用于从str获取值
        self.jsongetter = jsongetter  # 用于从json获取值
        self.default = default
        self.queryname = queryname  # 用于指定前端使用的名称
        self.doc = doc


def is_model_type(vartype):
    return hasattr(vartype, '__tablename__')


def choose_model_param(ctx: Context, modelCls):
    """
    >>> from sqlalchemy import Column, Integer
    >>> from sqlalchemy.ext.declarative import declarative_base
    >>> double = lambda n: n + n
    >>> @_annotate(id=RestParam(getter=int, jsongetter=double, default=0))
    ... class Truck(declarative_base()):
    ...     __tablename__ = 'tbl_truck'
    ...     id = Column(Integer, primary_key=True)
    ...     lpn = Column(Integer)
    >>> ctx = Context()
    >>> ctx._fields = {}
    >>> ctx.field_input.update(lpn='888')
    >>> truck = choose_model_param(ctx, Truck)
    >>> assert truck.id == 0, truck.id
    >>> assert truck.lpn == 888, truck.lpn
    >>>
    >>> ctx.json_input = {'id': 4}
    >>> truck = choose_model_param(ctx, Truck)
    >>> assert truck.id == 8, truck.id
    >>> assert truck.lpn is None, truck.lpn
    """
    adapters: Dict[str, RestParam] = {}
    if 'init adapters':
        for k, v in get_annotations(modelCls).items():
            h, kk = k[:1], k[1:]
            if h == '@' and isinstance(v, RestParam):
                adapters[kk] = v
        keys = [x for x in modelCls.__dict__ if not x.endswith('__') and x[0] != '_']
        for key in keys:
            if key in adapters: continue
            vartype = getattr(modelCls, key).type.python_type
            adapters[key] = RestParam(getter=vartype)

    model = modelCls()
    for name, adapter in adapters.items():
        try:
            if name in ctx.input:
                value = ctx.input[name]
            else:
                value = ctx.field_input.get(name, _nil)
                if value is _nil:
                    value = adapter.default
                elif ctx.is_json_request():
                    if adapter.jsongetter:
                        value = adapter.jsongetter(value)
                    else:
                        pass  # (value = value)
                else:
                    value = adapter.getter(value)

            setattr(model, name, value)
        except (ValueError, TypeError) as e:
            raise BadRequestError(text="Value Error ({}): {}".format(name, str(e)))
    return model


# 框架获取参数（重点）
def choose_param(ctx: Context, fn):
    """
    >>> from sqlalchemy import Column, Integer
    >>> from sqlalchemy.ext.declarative import declarative_base
    >>> double = lambda n: n + n
    >>> @_annotate(id=RestParam(getter=int, jsongetter=double, default=10))
    ... class Truck(declarative_base()):
    ...     __tablename__ = 'tbl_truck'
    ...     id = Column(Integer, primary_key=True)
    ...     lpn = Column(Integer)
    >>> @_annotate(pageNo=RestParam(getter=int, jsongetter=double, default=1))
    ... def controller(ctx, truck: Truck, pageNo, pageSize:int=10):
    ...     pass
    >>> ctx = Context()
    >>> ctx._fields = {}
    >>> ctx.field_input.update(lpn='88', pageNo='3')
    >>> truck = choose_model_param(ctx, Truck)
    >>> ret = choose_param(ctx, controller)
    >>> assert ret['truck'].id == 10, ret['truck'].id
    >>> assert ret['truck'].lpn == 88, ret['truck'].lpn
    >>> assert ret['pageNo'] == 3, ret['pageNo']
    >>> assert ret['pageSize'] == 10, ret['pageSize']
    >>>
    >>> ctx.json_input = {'id': 6, 'pageNo': 9, 'pageSize': 7}
    >>> ret = choose_param(ctx, controller)
    >>> assert ret['truck'].id == 12, ret['truck'].id
    >>> assert ret['truck'].lpn is None, ret['truck'].lpn
    >>> assert ret['pageNo'] == 18, ret['pageNo']
    >>> assert ret['pageSize'] == 7, ret['pageSize']
    """
    adapters: Dict[str, RestParam] = {}
    if 'init adapers':
        for key, anno, default in get_func_parameters(fn)[1:]:
            vartype = str if anno is _nil else anno
            default = None if default is _nil else default
            adapters[key] = RestParam(getter=vartype, default=default)
        for k, v in get_annotations(fn).items():
            h, kk = k[:1], k[1:]
            if h == '@' and isinstance(v, RestParam):
                adapters[kk] = v
    result = {}
    for name, adapter in adapters.items():
        queryname = adapter.queryname if getattr(adapter, 'queryname', None) else name
        # 如果是Model，只做平铺取值，且不允许设置queryname
        try:
            if queryname in ctx.input and not is_model_type(adapter.getter):
                value = ctx.input[queryname]
            elif not is_model_type(adapter.getter):
                value = ctx.field_input.get(queryname, _nil)
                if value is _nil:
                    value = adapter.default
                elif ctx.is_json_request():
                    if adapter.jsongetter:
                        value = adapter.jsongetter(value)
                    else:
                        pass  # (value = value)
                else:
                    value = adapter.getter(value)
            else:  # is_model_type(adapter.getter):
                value = choose_model_param(ctx, adapter.getter)
            result[name] = value
        except (ValueError, TypeError) as e:
            raise BadRequestError(text="Value Error [{}]: {}".format(queryname, str(e)))
    return result


def build_controller(fn):
    """
    >>> def controller(ctx, id:int, lpn):
    ...     return {'ctx': ctx, 'id': id, 'lpn': lpn}
    >>> ctx = Context()
    >>> ctx._fields = {}
    >>> ctx.field_input.update(id='5', lpn='HK888', pageNo='3')
    >>> ret = build_controller(controller)(ctx)
    >>> assert ret == {'ctx': ctx, 'id': 5, 'lpn': 'HK888'}, ret
    """
    def _1_controller(ctx):
        params = choose_param(ctx, fn)
        return fn(ctx, **params)

    return _1_controller


def interceptor(hook):
    def _1_wrapper(fn):
        def _1_1_controller(ctx):
            ctx.app_stack.append(build_controller(fn))
            params = choose_param(ctx, hook)
            result = hook(ctx, **params)
            ctx.app_stack.pop()  # 有多次调用ctx()的可能性，比如批量删除
            return result

        _1_1_controller.doc_stack = [fields_doc(hook)] + _eafp(lambda: fn.doc_stack, [fields_doc(fn)])
        return _1_1_controller

    return _1_wrapper


def modelview_controller(modelViewClass):
    def _1_wrapper(f):
        return modelViewClass.controller

    return _1_wrapper


class application(object):
    def __init__(self):
        self.mapping = []
        self.interceptors = []
        self.serializers = []

    def load(self, env):
        ctx = Context()
        ctx.environ = ctx.env = env
        ctx.host = env.get('HTTP_HOST')
        if env.get('wsgi.url_scheme') in ['http', 'https']:
            ctx.protocol = env['wsgi.url_scheme']
        elif env.get('HTTPS', '').lower() in ['on', 'true', '1']:
            ctx.protocol = 'https'
        else:
            ctx.protocol = 'http'
        ctx.homedomain = ctx.protocol + '://' + env.get('HTTP_HOST', '[unknown]')
        ctx.homepath = os.environ.get('REAL_SCRIPT_NAME', env.get('SCRIPT_NAME', ''))
        ctx.home = ctx.homedomain + ctx.homepath
        # @@ home is changed when the request is handled to a sub-application.
        # @@ but the real home is required for doing absolute redirects.
        ctx.realhome = ctx.home
        ctx.ip = env.get('REMOTE_ADDR')
        ctx.method = env.get('REQUEST_METHOD')
        ctx.path = env.get('PATH_INFO')
        # http://trac.lighttpd.net/trac/ticket/406 requires:
        if env.get('SERVER_SOFTWARE', '').startswith('lighttpd/'):
            ctx.path = env.get('REQUEST_URI').split('?')[0][:len(ctx.homepath)]
            # unquote explicitly for lighttpd to make ctx.path uniform across all servers.
            from urllib.parse import unquote
            ctx.path = unquote(ctx.path)

        ctx.query = env.get('QUERY_STRING')
        ctx.fullpath = ctx.path + '?' + ctx.query if ctx.query else ctx.path
        return ctx

    def handle_with_hooks(self, ctx):
        def _1_mapping_match():
            for mapping in self.mapping:
                _ = mapping.patternobj.search(ctx.path)
                if _ and (mapping.method == ctx.method or mapping.method == '*'):
                    ctx.url_input = _.groupdict()
                    return mapping.fn
            raise HttpError(status_code=404, text='Not Found', headers={})

        try:
            f = build_controller(_1_mapping_match())
            for hook in self.interceptors:
                if ctx.path.startswith(hook.prefix) and (hook.method == ctx.method or hook.method == '*'):
                    f = interceptor(hook.fn)(f)
            return f(ctx)
        except HttpError as e:
            e.update(ctx)
            return e.text

    def add_interceptor(self, prefix, method, fn):
        self.interceptors.insert(0, Interceptor(prefix, method, fn))

    def add_mapping(self, pattern, method, fn, doc=''):
        method = method.upper()
        patternobj = re.compile('^' + pattern + '$')
        if _is(ModelView)(fn):
            fn = fn.controller
        self.mapping.append(Mapping(pattern, method, fn, doc, patternobj))

    def add_serializer(self, varclass, fn):
        assert isinstance(varclass, type) or \
               (isinstance(varclass, tuple) and all(isinstance(x, type) for x in varclass)), \
            str(varclass)
        self.serializers.append(Serializer(varclass, fn))

    def serialize(self, obj):
        serializers = self.serializers
        class _1_Encoder(json.JSONEncoder):
            def default(self, obj):
                for f in serializers:
                    if isinstance(obj, f.varclass):
                        return f.fn(obj)
                return json.JSONEncoder.default(self, obj)

        return json.dumps(obj, cls=_1_Encoder).encode('utf-8')

    def wsgifunc(self, *middleware):
        def wsgi(env, start_resp):
            def _1_peep(iterator):
                """Peeps into an iterator by doing an iteration
                and returns an equivalent iterator.
                """
                # wsgi requires the headers first
                # so we need to do an iteration
                # and save the result for later
                try:
                    firstchunk = next(iterator)
                except StopIteration:
                    firstchunk = ''
                return itertools.chain([firstchunk], iterator)

            ctx = self.load(env)
            ctx.tail = '!'
            try:
                _ = self.handle_with_hooks(ctx)
                result = _1_peep(_) if isinstance(_, GeneratorType) else (_,)
            except Exception as e:  #todo
                import logging
                logging.exception(e)
                ctx.status_code, ctx.reason = 500, 'Internal Server Error'
                result = (str(e),)

            def _2_build_result(result):
                for r in result:
                    if isinstance(r, bytes):
                        yield r
                    elif isinstance(r, str):
                        yield r.encode('utf-8')
                    elif r is None:
                        yield b''
                    else:
                        yield self.serialize(r)

            result = _2_build_result(result)
            status = '{0} {1}'.format(ctx.status_code, ctx.reason)
            ctx.headers.setdefault('Content-Type', 'text/html')
            headers = list(ctx.headers.items())
            start_resp(status, headers)
            return itertools.chain(result, (b'',))

        for m in middleware:
            wsgi = m(wsgi)

        return wsgi

    def add_apidoc(self, prefix='/apidoc'):
        def _1_api_list(ctx):
            return mapping_list_doc(self.mapping, prefix)

        def _2_controller_detail(ctx):
            name = ctx.url_input['name']
            return controller_detail_doc(self.mapping, name)

        prefix @= prefix[:-1] | _if(prefix.endswith('/'))
        self.add_mapping(pattern=prefix + "/index.html", method='GET', fn=_1_api_list)
        self.add_mapping(pattern=prefix + r"/api_(?P<name>.+)\.html", method='GET', fn=_2_controller_detail)

    def run(self, port=None):
        from aiohttp import web
        from aiohttp_wsgi import WSGIHandler
        app = web.Application()
        app.router.add_route("*", "/{path_info:.*}", WSGIHandler(self.wsgifunc()))
        web.run_app(app, port=port)
