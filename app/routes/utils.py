from functools import wraps
from flask import make_response, abort, current_app
from flask_login import current_user
import os
from werkzeug.utils import secure_filename

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return no_cache


def role_required(role):
    def decorator(f):
        @wraps(f)   # ensure function name and docstring of f are preserved in wrapped
        def wrapped(*args, **kwargs):
            if current_user.user_type != role:
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return decorator



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(upload_file):
    if upload_file and upload_file.filename != "":
        if allowed_file(upload_file.filename):
            filename = secure_filename(upload_file.filename)
            upload_path = os.path.join(current_app.root_path, 'static/uploads', filename)

            os.makedirs(os.path.dirname(upload_path), exist_ok=True)

            upload_file.save(upload_path)
            return filename
        else:
            return None
    return None

