from flask import abort, session, redirect, request

def check_csrf_token(request):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)