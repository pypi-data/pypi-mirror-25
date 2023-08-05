from flask import has_request_context, _request_ctx_stack, current_app
from functools import wraps
from werkzeug.local import LocalProxy

current_authenticated_entity = LocalProxy(lambda: _get_authenticated_entity())


def _get_authenticated_entity():
    if has_request_context() and not hasattr(_request_ctx_stack.top, 'authenticated_entity'):
        current_app.auth_manager._load_authenticated_entity()

    return getattr(_request_ctx_stack.top, 'authenticated_entity', None)


def _context_processor():
    return dict(current_authenticated_entity=_get_authenticated_entity())

# def auth_required(func):
#     @wraps(func)
#     def decorated_view(*args, **kwargs):
#         if not current_authenticated_entity:
#             return current_app.auth_manager.unauthorized()
#         return func(*args, **kwargs)
#     return decorated_view


def privilege_required(*privileges):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            for privilege in privileges:
                if privilege.check():
                    return f(*args, **kwargs)
            return current_app.auth_manager.unauthorized()
        return wrapped
    return wrapper
