from flask import abort, session, redirect, request
from functools import wraps

def check_csrf_token(request):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") is None:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function