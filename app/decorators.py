from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission
'''
К функциям представления, которые должны быть доступны толь-
ко пользователям с определенными привилегиями, можно применять
собственный декоратор.
@permission_required(Permission.MODERATE_COMMENTS)
'''


# Декоратор проверки доступа
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# Декоратор проверки админки
def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)