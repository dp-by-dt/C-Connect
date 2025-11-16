#routes for taking the database data of users and display the profiles of the users in the discover page
from . import discover
from flask import render_template
from flask_login import login_required, current_user
from models import User  # For user discovery feature
# NEW ROUTE: User discovery page


@discover.route('/users')
@login_required
def users():
    # Fetch all users except the current user
    # REASON: Users shouldn't see themselves in discovery
    users = User.query.filter(User.id != current_user.id).all() #later need to add some algo for sorting the users to relation order
    return render_template('discover/users.html', users=users)