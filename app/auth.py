from functools import wraps
from firebase_admin import auth
from flask import request, redirect, session, url_for, flash
from functools import wraps

def login_required(route_func):
    @wraps(route_func)
    def decorated_route(*args, **kwargs):
        try:
            id_token = request.cookies.get('id_token')
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            # Check if user is authorized
            return route_func(*args, **kwargs)
        except auth.AuthError as e:
            # TODO: Handle authentication error
            return redirect('/login')  # Redirect to login page on authentication failure
    return decorated_route

def email_verified_required(view_func):
    @wraps(view_func)
    def decorated_function(*args, **kwargs):
        if "user_id" in session:
            user = auth.get_user(session["user_id"])
            if not user.email_verified:
                flash("Please verify your email address before proceeding.", "warning")
                return redirect(url_for("auth.verify_email"))
        return view_func(*args, **kwargs)
    return decorated_function
