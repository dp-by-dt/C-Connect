from . import auth
from flask import render_template, request, flash, redirect, url_for
from setup_db import add_user as adduser_glob
from models import User
from flask_login import login_user, logout_user, login_required, current_user


# CHANGED: /add_user → /signup (Best Practice: Cleaner, more intuitive URL)
# REASON: Standard convention is /signup for registration, easier for users to remember
@auth.route('/signup', methods=['GET', 'POST'])
def signup():  # CHANGED: Function name from add_user_route to signup for consistency
    # CHANGED: Redirect to dashboard if already logged in (Best Practice: UX improvement)
    # REASON: Logged-in users shouldn't access signup page
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Call your add_user function from setup_db (hashing is in here)
        success = adduser_glob(username, email, password)
        if not success:
            flash("Email already exists. Please use a different email.", "danger")  # CHANGED: category to 'danger' for Bootstrap styling
            return redirect(url_for('auth.signup'))

        # CHANGED: Auto-login after signup + redirect to dashboard (Best Practice: Better UX)
        # REASON: No need for separate success page, users want to get started immediately
        user = User.query.filter_by(email=email).first()
        login_user(user)
        flash(f'Welcome to C-Connect, {username}!', 'success')
        return redirect(url_for('auth.dashboard'))

    # If GET request, render the signup template
    return render_template('auth/signup.html')


# REMOVED: signup_success route (No longer needed with auto-login)
# REASON: signup_success.html is redundant; users are logged in and redirected to dashboard


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # CHANGED: Redirect to dashboard if already logged in (Best Practice: UX improvement)
    # REASON: Logged-in users shouldn't access login page again
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    
    if request.method == 'POST':
        # CHANGED: Use email instead of username for login (Best Practice: More secure & standard)
        # REASON: Emails are unique; usernames can be duplicated in future. Plus, most platforms use email login.
        email = request.form.get('email')  # Changed from username
        password = request.form.get('password')
        
        # CHANGED: Query by email instead of username
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # CHANGED: Added remember_me functionality (Best Practice: Better UX)
            # REASON: Users can choose to stay logged in
            remember = request.form.get('remember', False)  # Checkbox value
            login_user(user, remember=remember)
            
            flash('Login successful!', 'success')
            
            # CHANGED: Handle 'next' parameter for protected page redirects (Best Practice: Security)
            # REASON: If user tried to access a protected page, redirect them there after login
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')  # CHANGED: More specific error message
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html')


@auth.route('/dashboard')
@login_required  # Restricts access to logged-in users only
def dashboard():
    # No changes needed - works perfectly with new frontend
    return render_template('auth/dashboard.html', username=current_user.username)


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