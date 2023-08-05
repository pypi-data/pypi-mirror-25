import sqlalchemy
from salar.application import Context
from salar.sugar import *
from salar.webapi import BadRequestError, HttpError
import time
import hashlib


def safe_setattr(item, key, value):
    if key and hasattr(item, key):
        setattr(item, key, value)


def nowtimestamp():
    """获得当前UNIX时间戳(单位:秒)"""
    return int(time.time())


def build_filter_params(modelClass, item, filter_fields, optional=True):
    ret = []
    for key in filter_fields:
        if key.startswith('!'): opt, key = '!', key[1:]
        elif key.startswith('in:'): opt, key = 'in', key[3:]
        else: opt, key = '', key

        if optional and getattr(item, key, None) is None: continue

        if getattr(item, key, None) is None:
            ret.append(getattr(modelClass, key).in_(()))
        elif opt == '!':
            ret.append(getattr(modelClass, key) != getattr(item, key))
        elif opt == 'in':
            ret.append(getattr(modelClass, key).contains(getattr(item, key)))
        else:
            ret.append(getattr(modelClass, key) == getattr(item, key))
    return ret


class UpdateModelView(object):
    def __init__(
            self, modelClass, key_field='id', filter_fields=('id',), skip_fields=(), update_fields=(), incre_fields={},
            time_fields=('createAt', 'updateAt'), unique_fields=(), validate=(lambda old, new: None), return_key=False,
    ):
        def _1_controller(ctx, item: modelClass):
            query = ctx.db.query(modelClass)
            affected = 0
            for cp_item in query.filter(*build_filter_params(modelClass, item, filter_fields, optional=False)):
                try:
                    validate(cp_item, item)
                except (ValueError, TypeError) as e:
                    raise BadRequestError('invalid update: ' + str(e))

                for key in item.__annotations__:  # 以下情况不更新属性
                    if ((update_fields and key not in update_fields) or  # 不在update_fields中
                            (key in skip_fields) or    # 在skip_fields中
                            (time_fields and key == time_fields[0]) or   # 是createAt
                            (getattr(item, key) is None)):    # 值为None
                        continue

                    if key in incre_fields:  # 原值基础上自增或自减
                        setattr(cp_item, key, getattr(cp_item, key) + incre_fields[key])
                    else:  # 用新值更新原值
                        setattr(cp_item, key, getattr(item, key))

                with _catch():
                    safe_setattr(cp_item, time_fields[1], nowtimestamp())
                affected += 1

            if unique_fields:
                n = query.filter(*build_filter_params(modelClass, item, unique_fields, optional=False)).count()
                if n > 1:
                    ctx.rollback()
                    raise HttpError(409, 'unique conflict after update')
            if affected:
                ctx.need_commit = True
            ret = dict(code=0, message='ok', affected=affected)
            if return_key:
                ret[key_field] = getattr(item, key_field)
            return ret

        self.controller = _1_controller


class InsertModelView(object):
    def __init__(self, modelClass, key_field='id', time_fields=('createAt', 'updateAt'), unique_fields=(), return_key=False, validate=(lambda new: None)):
        def _1_controller(ctx, item: modelClass):
            try:
                validate(item)
            except (ValueError, TypeError) as e:
                raise BadRequestError('invalid insert: ' + str(e))

            with _catch(default=nowtimestamp()) as now:
                safe_setattr(item, time_fields[0], now)
                safe_setattr(item, time_fields[1], now)

            ctx.db.add(item)
            if unique_fields:
                n = ctx.db.query(modelClass).filter(*build_filter_params(modelClass, item, unique_fields, optional=False)).count()
                if n > 1:
                    ctx.rollback()
                    raise HttpError(409, 'unique conflict after create')
            ret = dict(code=0, message='ok')
            if return_key:
                ctx.db.commit()
                ctx.need_commit = False
                ret[key_field] = getattr(item, key_field)
            else:
                ctx.need_commit = True
            return ret

        self.controller = _1_controller


class DeleteModelView(object):
    def __init__(self, modelClass, filter_fields=('id',), validate=(lambda old: None)):
        def _1_controller(ctx, item: modelClass):
            query = ctx.db.query(modelClass)
            affected = 0
            for cp_item in query.filter(*build_filter_params(modelClass, item, filter_fields, optional=False)):
                try:
                    validate(cp_item)
                except (ValueError, TypeError) as e:
                    raise BadRequestError('invalid delete: ' + str(e))

                ctx.db.delete(cp_item)
                affected += 1

            if affected:
                ctx.need_commit = True
            return dict(code=0, message='ok', affected=affected)

        self.controller = _1_controller


class ListModelView(object):
    def __init__(
            self, modelClass, filter_fields=(), order_fields=('-id',),
            listall=False, default_page_size=10, max_page_size=100,
    ):
        def _1_controller(
                ctx,
                item: modelClass,
                pageNo: int = 1,
                pageSize: int = default_page_size,
        ):
            if hasattr(ctx, 'filter_kw'):
                filter_kw = ctx.filter_kw
            else:
                filter_kw = build_filter_params(modelClass, item, filter_fields)
            order_kw = []
            for key in order_fields:
                if key[0] == '-':
                    key = key[1:]
                    order_kw.append(sqlalchemy.desc(getattr(modelClass, key)))
                else:
                    key = key[1:] if key[0] == '+' else key
                    order_kw.append(getattr(modelClass, key))

            query_count = ctx.db.query(modelClass)
            query_paged = ctx.db.query(modelClass)
            if filter_kw:
                query_count = query_count.filter(*filter_kw)
                query_paged = query_paged.filter(*filter_kw)
            if order_kw:
                query_paged = query_paged.order_by(*order_kw)

            total_count = query_count.count()
            if listall:
                pageNo, pageSize = max(pageNo, 1), total_count
                cp_items = query_paged.all()
            else:
                pageNo, pageSize = max(pageNo, 1), min(max(pageSize, 1), max_page_size)
                cp_items = query_paged.offset((pageNo - 1) * pageSize).limit(pageSize).all()
            return dict(
                code=0,
                list=cp_items,
                pager=dict(pageNo=pageNo, pageSize=pageSize, totalCount=total_count),
            )

        self.controller = _1_controller


class DetailModelView(object):
    def __init__(self, modelClass, filter_fields=('id',),):
        def _1_controller(ctx, item: modelClass):
            filter_kw = build_filter_params(modelClass, item, filter_fields)
            cp_item = ctx.db.query(modelClass).filter(*filter_kw).first()
            return dict(
                code=0,
                detail=cp_item,
            )

        self.controller = _1_controller


class LoginModelView(object):
    def __init__(self, modelClass, login_field='username', key_field='adminId', expire_days=15, token_salt='80fb34'):
        def _1_build_hashed_token(admin_id, now):
            _ = token_salt + '{},{}'.format(admin_id, now)
            return hashlib.sha3_256(_.encode()).hexdigest()

        def _1_controller(
                ctx,
                item: modelClass,
                scene = login_field,
        ):
            try:
                admin = ctx.db.query(modelClass).filter_by(
                    **{scene: getattr(item, scene), 'password': item.password}
                ).one()
            except:
                raise HttpError(401, 'password not match')
            now = int(time.time())
            admin_id = getattr(admin, key_field)
            token = '{}-{}-{}'.format(_1_build_hashed_token(admin_id, now), admin_id, now)
            return {'code': 0, 'token': token, key_field: admin_id}

        def _1_interceptor(ctx: Context):
            token = ctx.get_header('HEADER', '')
            _ = token.split('-', 2)
            hashed_token, admin_id, login_at = _ if len(_) == 3 else ('', '0', '0')
            if _1_build_hashed_token(admin_id, login_at) != hashed_token:
                raise HttpError(401, 'invalid token')
            admin_id = int(admin_id)
            login_at = int(login_at)
            if int(time.time()) - login_at > expire_days * 86400:
                raise HttpError(401, 'expired')
            admin = ctx.db.query(modelClass).filter_by(**{key_field: admin_id}).first()
            if not admin:
                raise HttpError(401, 'not found admin error')
            ctx.me = admin
            return ctx()

        self.controller = _1_controller
        self.interceptor = _1_interceptor


class PermitModelView(object):
    def __init__(self, path_permits, role_field='role'):
        """
        :param path_permits: [{prefix:str, role:int, methods:[str...], fields:[str...]} ...]
        for example:
            [
                {'/manage/client', role:1, methods:['POST'], fields:['companyId->cid', 'adminId']},
            ... ]
        """
        def _1_interceptor(ctx):
            debug_msg = ':'
            if ctx.me is None:
                raise HttpError(401, 'need login')
            for permit in path_permits:
                if not ctx.path.startswith(permit['prefix']): continue
                role = getattr(ctx.me, role_field)
                debug_msg += '{}'.format(ctx.me)
                if role != permit['role']:
                    debug_msg += ' ; S1: {}'.format(permit['role'])
                    continue
                if 'methods' in permit and ctx.method not in permit['methods']:
                    debug_msg += ' ; S2: {}'.format(permit['methods'])
                    continue
                for key in permit.get('fields', []):
                    key_me, key_query = key.split.split('->') if '->' in key else (key, key)
                    ctx.input[key_query] = getattr(ctx.me, key_me)
                return ctx()
            raise HttpError(403, debug_msg)

        self.interceptor = _1_interceptor
