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
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.user_type != role:
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return decorator



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(image_file):
    if image_file and image_file.filename != "":
        if allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            upload_path = os.path.join(current_app.root_path, 'static/uploads', filename)

            
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)

            image_file.save(upload_path)
            return filename 
        else:
            return None 
    return None

