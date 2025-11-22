from . import auth
from flask import render_template, request, flash, redirect, url_for, render_template, request
from setup_db import add_user as adduser_glob
from models import User, Profile
from flask_login import login_user, logout_user, login_required, current_user
from extensions import login_manager, db
from .forms import SignupForm, LoginForm, EditProfileForm
from urllib.parse import urlparse, urljoin
from flask import current_app as app


import os
from werkzeug.utils import secure_filename
from datetime import datetime, timezone


# ------- functions --------
def is_safe_url(target): #check the sanity of links
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http','https') and ref_url.netloc == test_url.netloc




ALLOWED_EXT = {'png','jpg','jpeg','webp'}

def save_profile_picture(file_storage, user_id):
    """Save uploaded file to UPLOAD_FOLDER; return relative url path"""
    filename = secure_filename(file_storage.filename)
    # make filename unique: userID + timestamp + original

    name, ext = os.path.splitext(filename)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    filename = f"user{user_id}_{timestamp}{ext}"

    upload_folder = app.config.get('UPLOAD_FOLDER') or os.path.join(app.static_folder, 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, filename)
    file_storage.save(filepath)

    # return a path suitable for <img src=>, e.g. "/static/uploads/..."
    # if UPLOAD_FOLDER is inside static, return url relative to root
    if upload_folder.startswith(app.static_folder):
        rel = os.path.relpath(filepath, app.static_folder)
        return f"/static/{rel.replace(os.path.sep, '/')}"
    return filepath  # absolute path (not ideal for web serving)


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
    profile = current_user.profile
    # display default placeholders if None
    return render_template('auth/profile.html', profile=profile, user=current_user)


# NEW ROUTE: Profile edit (for future implementation)
# REASON: Separating view and edit is good practice; ready for future profile update functionality

@auth.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    profile = current_user.profile
    if not profile:
        # Shouldn't happen if you create profile at signup, but safe fallback
        profile = Profile(user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()

    form = EditProfileForm(obj=profile)

    if form.validate_on_submit():
        # Basic sanitization
        username = form.username.data.strip() if form.username.data else current_user.username
        department = form.department.data.strip() if form.department.data else None
        year = form.year.data.strip() if form.year.data else None
        bio = form.bio.data.strip() if form.bio.data else None
        location = form.location.data.strip() if form.location.data else None

        # interests: turn comma-separated into list (JSON)
        interests_raw = form.interests.data or ""
        interests_list = [i.strip() for i in interests_raw.split(',') if i.strip()]
        if len(interests_list) == 0:
            interests_val = None
        else:
            interests_val = interests_list

        # check username uniqueness (if changed)
        if username != current_user.username:
            if User.query.filter(User.username == username, User.id != current_user.id).first():
                form.username.errors.append("Username already taken.")
                return render_template('auth/profile_edit.html', form=form)

        # handle profile picture
        if form.profile_picture.data:
            file = form.profile_picture.data
            # optional: validate extension again
            ext = os.path.splitext(file.filename)[1].lower().lstrip('.')
            if ext not in ALLOWED_EXT:
                form.profile_picture.errors.append("Invalid image type.")
                return render_template('auth/profile_edit.html', form=form)
            pic_url = save_profile_picture(file, current_user.id)
            profile.profile_picture = pic_url

        # apply updates
        current_user.username = username
        profile.department = department
        profile.year = year
        profile.bio = bio
        profile.location = location
        profile.interests = interests_val
        profile.updated_at = db.func.now()

        try:
            db.session.commit()
            flash("Profile updated successfully.", "success")
            return redirect(url_for('auth.profile'))
        except Exception as exc:
            db.session.rollback()
            app.logger.exception("Failed to update profile for user %s: %s", current_user.email, exc)
            flash("An error occurred while saving profile.", "danger")
            return render_template('auth/profile_edit.html', form=form)

    # populate interests field for display (join with comma)
    if request.method == 'GET':
        if profile.interests:
            if isinstance(profile.interests, list):
                form.interests.data = ", ".join(profile.interests)
            else:
                # if stored as raw text, leave it
                form.interests.data = profile.interests

    return render_template('auth/profile_edit.html', form=form)