from flask import abort, session, redirect, request
from functools import wraps

def check_csrf_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == "POST":
            if not request.form.get("csrf_token") or session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") is None:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function