from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.models import Users
from werkzeug.security import check_password_hash


bp = Blueprint("bp", __name__)


@bp.route("/")
def starting_url():
    return redirect(url_for('bp.login_get'))



@bp.route("/login", methods=['GET'])
def login_get():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('bp.home'))
    except Exception as e:
        flash(f"An error occurred during login: {str(e)}", "danger")
    
    return render_template('login.html')


@bp.route("/login", methods=['POST'])
def login_post():
    try:
        user = Users.query.filter_by(username=request.form['username']).first()

        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('bp.home'))
        else:
            flash("Invalid Credentials", "danger")
    except Exception as e:
        flash(f"An error occurred during login: {str(e)}", "danger")

    return redirect(url_for('bp.login_get'))




@bp.route("/home")
@login_required
def home():
    try:
        if current_user.user_type == 'Admin':
            return render_template("admin_home.html")
        elif current_user.user_type == 'Client':
            return render_template("user_home.html")
        else:
            flash("Unknown user type.", "danger")
            return "Unknown user type", 403

    except Exception as e:
        flash(f"An error occurred while loading the home page: {str(e)}", "danger")
        return render_template("error.html"), 500  # can create an error.html template

    


@bp.route("/logout")
@login_required
def logout():
    try:
        logout_user()
        flash("You have been logged out successfully.", "success")
        return redirect(url_for('bp.login_get'))
    
    except Exception as e:
        flash(f"An error occurred during logout: {str(e)}", "danger")
        return redirect(url_for('bp.home'))
    



@bp.route("/profile")
@login_required
def profile():
    try:
        user = Users.query.filter_by(id=current_user.id).first()
        
        if user:
            return render_template("profile.html", user=user)
        else:
            flash("User not found", "danger")
            return redirect(url_for('bp.home'))
    
    except Exception as e:
        flash(f"An error occurred while fetching the user profile: {str(e)}", "danger")
        return redirect(url_for('bp.home'))

