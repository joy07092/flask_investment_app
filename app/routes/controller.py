from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.models import Users, Clients, Deposits, Deposit_Logs
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timezone
from .utils import nocache, role_required, save_file
from app import db

bp = Blueprint("bp", __name__)


@bp.route("/")
def starting_url():
    return redirect(url_for('bp.login_get'))



@bp.route("/login", methods=['GET'])
@nocache
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

        if user:
            if user.status.lower() == 'inactive':
                flash("Your account is inactive. Please contact the administrator.", "warning")
                return redirect(url_for('bp.login_get'))

            if check_password_hash(user.password, request.form['password']):
                login_user(user)
                return redirect(url_for('bp.home'))

        flash("Invalid credentials", "danger")

    except Exception as e:
        flash(f"An error occurred during login: {str(e)}", "danger")

    return redirect(url_for('bp.login_get'))



@bp.route("/home")
@login_required
@nocache
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



@bp.route("/users")
@login_required
@role_required('Admin')
def users():
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            #flash("Direct access to this page is not allowed.", "warning")
            return redirect(url_for('bp.home'))
    
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        users = Users.query.paginate(page=page, per_page=per_page)
        return render_template('users.html', users=users)
    except Exception as e:
        flash("Failed to retrieve users.", "danger")
        return redirect(url_for('bp.home'))
    


@bp.route("/change_user_password", methods=["GET"]) #admin changing from table
@login_required
@role_required("Admin")
def change_user_password_get():
    user_id = request.args.get("user_id")
    if not user_id:
        flash("User ID is required.", "danger")
        return redirect(url_for("bp.home"))  

    user = Users.query.get(user_id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("bp.home"))

    return render_template("change_user_password.html", user=user)



@bp.route("/change_user_password", methods=["POST"]) #admin changing from table
@login_required
@role_required("Admin")
def change_user_password_post():
    try:
        user_id = request.form.get("user_id")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not (new_password and confirm_password):
            flash("Both password fields are required.", "warning")
            return redirect(url_for("bp.home"))

        if new_password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("bp.home"))

        user = Users.query.get(user_id)
        if not user:
            flash("User not found.", "danger")
            return redirect(url_for("bp.home"))

        user.password = generate_password_hash(new_password)
        db.session.commit()

        flash(f"Password updated successfully for {user.username}.", "success")
    except Exception as e:
        flash(f"An error occurred while changing the password: {str(e)}", "danger")

    return redirect(url_for("bp.users"))



@bp.route('/change_user_status')
@login_required
@role_required('Admin')
def change_user_status():
    user_id = request.args.get('user_id')
    try:
        if not user_id:
            return "User ID missing", 400

        user = Users.query.get(user_id)
        if not user:
            return "User not found", 404

        
        user.status = 'Inactive' if user.status.lower() == 'active' else 'Active'
        db.session.commit()

        return redirect(url_for('bp.users')) 

    except Exception as e:
        flash("Failed to retrieve user.", "danger")
        return redirect(url_for('bp.home'))



@bp.route("/clients")
@login_required
@role_required('Admin')
def clients():
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return redirect(url_for('bp.home'))
    
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        clients = Clients.query.paginate(page=page, per_page=per_page)
        return render_template('clients.html', clients=clients)
    except Exception as e:
        flash("Failed to retrieve clients.", "danger")
        return redirect(url_for('bp.home'))



@bp.route('/client_details', methods=['GET'])
@login_required
@role_required('Admin')
def client_details():
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            #flash("Direct access to this page is not allowed.", "warning")
            return redirect(url_for('bp.home'))
    
    client_id = request.args.get('client_id')
    if not client_id:
        return "Client ID not provided", 400

    try:
        client = db.session.get(Clients, int(client_id))
        if not client:
            return "Client not found", 404
        return render_template('client_details.html', client=client)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500



@bp.route("/deposits")
@login_required
def deposits():
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return redirect(url_for('bp.home'))
    
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        if current_user.user_type.lower() == "admin":
            deposits = Deposits.query.order_by(Deposits.date.desc()).paginate(page=page, per_page=per_page)
        else:
            deposits = Deposits.query.filter_by(client_id=current_user.client_id)\
                                       .order_by(Deposits.date.desc())\
                                       .paginate(page=page, per_page=per_page)

        return render_template("deposits.html", deposits=deposits)

    except Exception as e:
        flash(f"Error loading deposits: {str(e)}", "danger")
        return redirect(url_for('bp.home'))




@bp.route("/update_deposit")
@login_required
def update_deposit():
    if not request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return redirect(url_for('bp.home'))

    try:
        deposit_id = request.args.get("deposit_id")
        if not deposit_id:
            flash("Deposit ID is missing.", "warning")
            return redirect(url_for('bp.home'))

        deposit = Deposits.query.get(deposit_id)
        if not deposit:
            flash("Deposit not found.", "danger")
            return redirect(url_for('bp.home'))

        return render_template("deposit_update.html", deposit=deposit)

    except Exception as e:
        flash("An error occurred while loading the deposit update form.", "danger")
        print("Error loading update deposit:", e)
        return redirect(url_for('bp.home'))



@bp.route("/update_deposit", methods=['POST'])
@login_required
def update_deposit_post():
    try:
        deposit_id = request.form.get("deposit_id")
        if not deposit_id:
            flash("Missing deposit ID.", "danger")
            return redirect(url_for('bp.home'))

        deposit = Deposits.query.get(deposit_id)
        if not deposit:
            flash("Deposit not found.", "danger")
            return redirect(url_for('bp.home'))

        
        deposit_log = Deposit_Logs(
            client_id=deposit.client_id,
            month=deposit.month.replace("-", ""),
            date=deposit.date.replace("-", ""),
            amount=deposit.amount,
            comments=deposit.comments,
            created_by=deposit.created_by,
            created_at=deposit.created_at,
            action_type="update",
            updated_at=datetime.now(timezone.utc),
            updated_by=current_user.username
        )

        
        deposit.client_id = request.form.get("client_id")
        deposit.month = request.form.get("month").replace("-", "") 
        deposit.date = request.form.get("date").replace("-", "") 
        deposit.amount = request.form.get("amount")
        deposit.comments = request.form.get("comments")

        
        file = request.files.get("file")
        if file and file.filename:
            filename = save_file(file)
            deposit.file = filename

        
        db.session.add(deposit_log)
        db.session.commit()

        flash("Deposit updated successfully and logged.", "success")
        return redirect(url_for('bp.home'))

    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while updating the deposit: {str(e)}", "danger")
        return redirect(url_for('bp.home'))



@bp.route("/delete_deposit")
@login_required
def delete_deposit():
    try:
        deposit_id = request.args.get("deposit_id")

        if not deposit_id:
            flash("Deposit ID is required.", "danger")
            return redirect(url_for("bp.home"))

        deposit = Deposits.query.get(deposit_id)

        if not deposit:
            flash("Deposit not found.", "danger")
            return redirect(url_for("bp.home"))

        
        deposit_log = Deposit_Logs(
            client_id=deposit.client_id,
            month=deposit.month,
            date=deposit.date,
            amount=deposit.amount,
            comments=deposit.comments,
            created_by=deposit.created_by,
            created_at=deposit.created_at,
            action_type="delete",
            updated_at=datetime.now(timezone.utc),
            updated_by=current_user.username
        )

        
        db.session.add(deposit_log)
        db.session.delete(deposit)
        db.session.commit()

        flash("Deposit deleted and logged successfully.", "success")
        return redirect(url_for("bp.home"))
    
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while deleting the deposit: {str(e)}", "danger")
        return redirect(url_for("bp.home"))

   

@bp.route("/deposit_logs")
@login_required
@role_required('Admin')
def deposit_logs():
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return redirect(url_for('bp.home'))

    try:
        page = request.args.get('page', 1, type=int) # If the URL is /logs?page=3, then page will be 3
        per_page = request.args.get('per_page', 10, type=int)

        logs = Deposit_Logs.query.order_by(Deposit_Logs.updated_at.desc()).paginate(page=page, per_page=per_page)
        # pagination object with attributes (items, page, pages, has_next, has_prev)

        return render_template('deposit_logs.html', logs=logs)
    except Exception as e:
        flash(f"Failed to load deposit logs: {str(e)}", "danger")
        return redirect(url_for('bp.home'))




@bp.route("/logout")
@login_required
def logout():
    try:
        logout_user()
        flash("You have been logged out successfully.", "success")
        response = redirect(url_for('bp.login_get'))
        response.headers['Cache-Control'] = 'no-store'
        return response
    
    except Exception as e:
        flash(f"An error occurred during logout: {str(e)}", "danger")
        return redirect(url_for('bp.home'))



@bp.route("/profile")
@login_required
def profile():
    try:
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            #flash("Direct access to this page is not allowed.", "warning")
            return redirect(url_for('bp.home'))

        user = Users.query.filter_by(id=current_user.id).first()

        if user:
            return render_template("profile.html", user=user)
        else:
            flash("User not found", "danger")
            return redirect(url_for('bp.home'))

    except Exception as e:
        flash(f"An error occurred while fetching the user profile: {str(e)}", "danger")
        return redirect(url_for('bp.home'))



@bp.route("/createClient", methods=["POST"])
@login_required
@role_required('Admin')
def createClient():
    try:
        
        name = request.form['name']
        mobile = request.form['mobile']
        nid = request.form['nid']
        status = request.form['status']

        
        existing_client = Clients.query.filter_by(name=name).first()
        if existing_client:
            flash("Client already exists", "warning")
            return redirect(url_for("bp.clients"))

        
        email = request.form['email'] or None
        emergency_contact = request.form['emergency_contact'] or None
        present_address = request.form['present_address'] or None
        permanent_address = request.form['permanent_address'] or None
        nominee_name = request.form['nominee_name'] or None
        nominee_nid = request.form['nominee_nid'] or None
        nominee_mobile = request.form['nominee_mobile'] or None

        
        image_file = request.files.get("image")
        image_filename = save_file(image_file) 

        
        new_client = Clients(
            name=name,
            mobile=mobile,
            nid=nid,
            status=status,
            email=email,
            emergency_contact=emergency_contact,
            present_address=present_address,
            permanent_address=permanent_address,
            nominee_name=nominee_name,
            nominee_nid=nominee_nid,
            nominee_mobile=nominee_mobile,
            image=image_filename,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            created_by=current_user.username,
            updated_by=None
        )

        
        db.session.add(new_client)
        db.session.commit()
        flash("Client created successfully", "success")
        return redirect(url_for("bp.clients"))

    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect(url_for("bp.clients"))



@bp.route("/createUser", methods=["POST"])
@login_required
@role_required('Admin')
def createUser():
    try:
        data = request.form

        user_type = data.get('user_type')
        username = data.get('username')
        email = data.get('email')
        mobile_number = data.get('mobile_number')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        status = data.get('status')
        client_id = data.get('client_id') if user_type == 'Client' else None

        

        
        if Users.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for("bp.users"))

        
        if user_type == 'Client':
            if not client_id or not client_id.isdigit():
                flash('Client ID must be a valid number.', 'danger')
                return redirect(url_for("bp.users"))

            client = Clients.query.get(int(client_id))
            if not client:
                flash('Client ID does not exist in the clients table.', 'danger')
                return redirect(url_for("bp.users"))

            
            existing_user = Users.query.filter_by(client_id=int(client_id)).first()
            if existing_user:
                flash('This Client ID is already assigned to another user.', 'danger')
                return redirect(url_for("bp.users"))

        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for("bp.users"))

        
        new_user = Users(
            user_type=user_type,
            username=username,
            email=email,
            mobile_number=mobile_number,
            password=generate_password_hash(password),
            status=status,
            client_id=int(client_id) if client_id else None,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            created_by=current_user.username,
            updated_by=None
        )

        db.session.add(new_user)
        db.session.commit()

        flash('User created successfully.', 'success')
        return redirect(url_for("bp.users"))

    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred while creating the user: {str(e)}', 'danger')
        return redirect(url_for("bp.users"))



@bp.route('/createDeposit', methods=['POST'])
@login_required
def createDeposit():
    try:
        client_id = request.form.get("client_id")
        month = request.form.get("month").replace("-", "")  # e.g., '2025-05' -> '202505'
        date = request.form.get("date").replace("-", "")    # e.g., '2025-05-17' -> '20250517'
        amount = request.form.get("amount")
        comments = request.form.get("comments")
        file = request.files.get("file")

        # Check if client_id exists in Clients table
        client = Clients.query.get(client_id)
        if not client:
            flash("No client exists with the provided Client ID.", "warning")
            return redirect(url_for('bp.deposits'))

        filename = save_file(file)

        new_deposit = Deposits(
            client_id=client_id,
            month=month,
            date=date,
            amount=amount,
            comments=comments,
            file=filename,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            created_by=current_user.username,
            updated_by=None
        )

        db.session.add(new_deposit)
        db.session.commit()
        flash("Deposit successfully created.", "success")
        return redirect(url_for('bp.home')) 

    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect(url_for('bp.deposits'))  



@bp.route('/changePassword', methods=['POST']) # user chaning their own password
@login_required
def changePassword():
    try:
        
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Check if the current password is correct
        if not check_password_hash(current_user.password, current_password):
            flash("Current password is incorrect.", "danger")
            return redirect(url_for('bp.profile'))

        # Check if new password and confirm password match
        if new_password != confirm_password:
            flash("New password and confirmation do not match.", "warning")
            return redirect(url_for('bp.profile'))

        # Update the password
        current_user.password = generate_password_hash(new_password)
        db.session.commit()

        flash("Password updated successfully.", "success")
        return redirect(url_for('bp.profile'))

    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while updating the password: {str(e)}", "danger")
        return redirect(url_for('bp.profile'))

    