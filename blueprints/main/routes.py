from . import main
from flask import render_template
from flask_login import login_required, current_user
from models import User  # For user discovery feature
from models import Connection  # For viewing other user's profile
from flask import redirect, url_for


# CHANGED: Render main/home.html instead of base.html (Best Practice: Proper template organization)
# REASON: base.html is the parent template; home.html should be the landing page content
@main.route('/')
def home():
    return render_template('main/home.html')


@main.route('/about')
def about():
    return render_template('main/about.html')


@main.route('/contact')
def contact():
    # CHANGED: Pass name parameter conditionally based on login status (Best Practice: Better UX)
    # REASON: Show user's name if logged in, otherwise show 'Guest'
    if current_user.is_authenticated:
        return render_template('main/contact.html', name=current_user.username)
    return render_template('main/contact.html', name='Guest')



@main.route('/dashboard')
@login_required  # Restricts access to logged-in users only
def dashboard():
    # No changes needed - works perfectly with new frontend
    return render_template('main/dashboard.html', username=current_user.username)


# NEW ROUTE: User discovery page
# REASON: Core feature for social network; allows users to find and connect with others
@main.route('/discover')
@login_required
def discover():
    # Fetch all users except the current user
    # REASON: Users shouldn't see themselves in discovery
    users = User.query.filter(User.id != current_user.id).all()
    return render_template('main/discover.html', users=users)


# NEW ROUTE: Messaging page (placeholder for now)
# REASON: Core feature for social network; will be implemented later
@main.route('/messages')
@login_required
def messages():
    # TODO: Implement messaging system with database models
    return render_template('main/messages.html')


# NEW ROUTE: Settings page
# REASON: Users need to manage their account preferences
@main.route('/settings')
@login_required
def settings():
    return render_template('main/settings.html')



#viewing other user's profile
@main.route("/user/<int:user_id>")
@login_required
def view_user_profile(user_id):
    if user_id == current_user.id:
        return redirect(url_for("auth.profile"))

    user = User.query.get_or_404(user_id)
    profile = user.profile

    # get connection object
    conn = Connection.query.filter(
        ((Connection.user_id == current_user.id) & (Connection.target_user_id == user_id)) |
        ((Connection.user_id == user_id) & (Connection.target_user_id == current_user.id))
    ).first()

    return render_template(
        "main/user_profile.html",
        user=user,
        profile=profile,
        conn=conn
    )
