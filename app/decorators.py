from functools import wraps
from urllib.parse import urlparse
from flask import redirect, request
from flask_login import current_user


def anonymous_user(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect("/")
        return f(*args, **kwargs)

    return decorated_func


def authenticated_user(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        parsed_url = urlparse(request.url)
        path = parsed_url.path
        if not current_user.is_authenticated:
            return redirect("/login?next=" + path)
        return f(*args, **kwargs)

    return decorated_func
