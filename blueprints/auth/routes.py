from . import auth
from flask import render_template, request, flash, redirect, url_for
from setup_db import add_user as adduser_glob
from models import User
from flask_login import login_user, logout_user, login_required, current_user
from extensions import login_manager, db
from .forms import SignupForm, LoginForm
from urllib.parse import urlparse, urljoin
from flask import current_app as app

# ------- functions --------
def is_safe_url(target): #check the sanity of links
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http','https') and ref_url.netloc == test_url.netloc



# CHANGED: /add_user → /signup (Best Practice: Cleaner, more intuitive URL)
# REASON: Standard convention is /signup for registration, easier for users to remember
@auth.route('/signup', methods=['GET', 'POST'])
def signup():  # CHANGED: Function name from add_user_route to signup for consistency
    # CHANGED: Redirect to dashboard if already logged in (Best Practice: UX improvement)
    # REASON: Logged-in users shouldn't access signup page
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    
    #using CSRF for login from the Class SignupForm
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip().lower()
        password = form.password.data

        #checking duplicate email form db
        success = adduser_glob(username, email, password)
        if not success: #if False: email already in db
            form.email.errors.append("This email is already registered.")
            #rendering template instead of redirect to keep form data
            return render_template('auth/signup.html',form=form)

        #adding user to db and logging in 
        user = User.query.filter_by(email=email).first()
        login_user(user)
        flash(f'Welcome to C-Connect, {username}!', 'success')
        return redirect(url_for('main.dashboard'))

    # If GET request or vadiation error, render the signup template
    return render_template('auth/signup.html',form=form)


# REMOVED: signup_success route (No longer needed with auto-login)
# REASON: signup_success.html is redundant; users are logged in and redirected to dashboard



@auth.route('/login', methods=['GET', 'POST'])
def login():
    # CHANGED: Redirect to dashboard if already logged in (Best Practice: UX improvement)
    # REASON: Logged-in users shouldn't access login page again
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    

    #using CSRF for login from the Class LoginForm
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        password = form.password.data
        remember = form.remember_me.data #checkbox data
        
        # CHANGED: Query by email instead of username
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # Update last_login timestamp
            user.last_login = db.func.now()
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                # optional: log error but still login_user (or decide to fail)
                app.logger.exception("Failed to update last_login for user %s", user.email)

            login_user(user, remember=remember)
            
            flash('Login successful!', 'success')
            
            # CHANGED: Handle 'next' parameter for protected page redirects (Best Practice: Security)
            # REASON: If user tried to access a protected page, redirect them there after login
            next_page = request.args.get('next')
            if next_page and is_safe_url(next_page): #check safety of url
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))

        #csrf form error handling
        form.email.errors.append("Invalid email or password.")

        # CHANGED: More specific error message
        return render_template('auth/login.html', form=form)

    return render_template('auth/login.html',form=form)




#for more clarity, use get and post methods here and also add a logout_confirmation html page which is triggered for confirmation before logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for('main.home'))  # CHANGED: Redirect to home instead of login (Best Practice: Better UX)
    # REASON: After logout, show the landing page, not login page


# NEW ROUTE: Profile page for viewing/editing user profile
# REASON: Essential for social network; allows users to update their information
@auth.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')


# NEW ROUTE: Profile edit (for future implementation)
# REASON: Separating view and edit is good practice; ready for future profile update functionality
@auth.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    if request.method == 'POST':
        # TODO: Implement profile update logic here
        # username = request.form.get('username')
        # bio = request.form.get('bio')
        # etc.
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/profile_edit.html')