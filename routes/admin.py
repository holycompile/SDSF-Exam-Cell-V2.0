from flask import Blueprint, render_template,request,redirect,flash,url_for,session
from databases.queries import validate_admin,check_username_exists,insert_in_admin
from functools import wraps
#Note in Flask: 
#url_for('blueprint_name.function_name' )
# for calling it next time use 
# url_for('admin.admin_login')

# 1. The Blueprint Name is 'admin'
admin_bp=Blueprint('admin', __name__, template_folder='../templates')


##################################################
# The Reusable Route Guard Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash("Unauthorized access. Please log in first.", "danger")
            # Captures where they tried to go (?next=/admin/dashboard)
            return redirect(url_for('admin.admin_login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function
##############################################################




# 2. The Function Name is 'admin_login'
@admin_bp.route('/login', methods=['GET','POST'])
def admin_login():
    msg=""
    # If already logged in, skip login page and go straight to dashboard
    if 'admin_id' in session:
        return redirect(url_for('admin.admin_dashboard'))
    
    # otherwise we shall tell them to login
    if request.method=='POST':
        username=request.form.get('username') # current username inputted by the user
        password=request.form.get('password') # current password entered by user 
        admin = validate_admin(username,password) # admin is now a single dictionary 
        if admin:
            session['admin_id'] = admin['id']
            session['admin_user'] = admin['username']
            flash("Login Successfull!")
            return redirect(url_for('admin.admin_dashboard'))
        else:
            return render_template("admin_login_page.html",msg="login error")
    return render_template("admin_login_page.html")




# Protected Admin Dashboard Route
@admin_bp.route('/dashboard', methods=['GET'])
@login_required  # <--- This ensures weather the admin is logged in or not One single word protects this entire route
def admin_dashboard():
    msg='logged in'
    return render_template("admin_dashboard.html", msg=msg)


# Admin Logout Route
@admin_bp.route('/logout', methods=['GET'])
def admin_logout():
    session.clear()
    flash("You have been successfully logged out.", "info")
    return redirect(url_for('admin.admin_login'))


#Admin Registration section 
@admin_bp.route("/registration", methods=['GET','POST'])
def admin_register():
    msg=None
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        #1st check weather this record already exists or not
        existing_user = check_username_exists(username)
        
        if existing_user: #which means soemthing dictionary has been returned hence the username exists
            flash("User already exists, try creating with a different username")
            return render_template("admin_registration_form.html", error="user already exists")
        else: # this means no such username exists till now in the database
            new_admin = insert_in_admin(username,password)
            if new_admin:
                flash("Admin registered successfully Pleaase login now ","success")
                return redirect(url_for('admin.admin_login'))
            else:
                return render_template("admin_registration_form.html",error="Registration Failed ")
         
    return render_template("admin_registration_form.html")
    