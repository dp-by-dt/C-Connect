from . import main
from flask import render_template, jsonify
from flask_login import login_required, current_user
from models import User, Profile, Post  # For user discovery feature
from models import Connection, ProfileVisit  # For viewing other user's profile
from flask import redirect, url_for
from extensions import db
from flask import abort
from flask import request
from flask import flash, session


from sqlalchemy import case, or_, and_, func
from utils.profile_completion import calculate_profile_completion

from datetime import datetime, timezone



#------------ Helper functions ---------
def get_connection_status(viewer_id, target_id):
    """For each of the user with other users
    Returns: 'connected', 'pending', 'rejected', or None"""

    conn = Connection.query.filter(
        ((Connection.user_id == viewer_id) & (Connection.target_user_id == target_id)) |
        ((Connection.user_id == target_id) & (Connection.target_user_id == viewer_id))
    ).first()
    
    if conn:
        if conn.status == 'accepted':
            return 'connected'
        elif conn.status == 'pending':
            return 'pending'
        elif conn.status == 'rejected':
            return 'rejected'
    return None




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
    user_id = current_user.id

    # count accepted connections (either side)
    accepted_count = db.session.query(Connection).filter(
        (Connection.status == 'accepted') & (
            (Connection.user_id == user_id) | (Connection.target_user_id == user_id)
        )
    ).count()

    # pending incoming
    pending_incoming = db.session.query(Connection).filter_by(
        target_user_id=user_id, status='pending'
    ).count()

    # pending outgoing
    pending_outgoing = db.session.query(Connection).filter_by(
        user_id=user_id, status='pending'
    ).count()

    # optionally other stats
    stats = {
        "connections": accepted_count,
        "pending_incoming": pending_incoming,
        "pending_outgoing": pending_outgoing
    }

    completion = calculate_profile_completion(user_profile=current_user.profile)

    #show flash message if the profile is complete
    if (completion["percentage"] == 100) and not session.get("profile_completed"):
        flash("Your profile is now complete!", "success")
        session["profile_completed"] = True

    if completion["percentage"] < 100:
        session.pop("profile_completed", None)


    return render_template('main/dashboard.html', 
                    username=current_user.username, 
                    stats=stats, posts=current_user.posts, 
                    profile_pic=current_user.profile.profile_picture, 
                    profile_completion=completion
                )




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

    #validate user_id
    if user_id <= 0 or user_id == current_user.id:
        return redirect(url_for("auth.profile"))


    user = User.query.get_or_404(user_id)
    profile = user.profile

    # get connection object
    conn = Connection.query.filter(
        ((Connection.user_id == current_user.id) & (Connection.target_user_id == user_id)) |
        ((Connection.user_id == user_id) & (Connection.target_user_id == current_user.id))
    ).first()


    #for showing the posts by the user
    posts = (
        Post.query
        .filter_by(user_id=user.id)
        .order_by(Post.created_at.desc())
        .limit(10)
        .all()
    )


    if current_user.id != user.id:
        try:
            # Prevent duplicate visits within last 30 minutes
            last_visit = (
                ProfileVisit.query
                .filter_by(viewer_id=current_user.id, viewed_id=user.id)
                .order_by(ProfileVisit.timestamp.desc())
                .first()
            )

            if not last_visit or (datetime.now(timezone.utc) - last_visit.timestamp).total_seconds() > 1800: #30 minutes
                v = ProfileVisit(viewer_id=current_user.id, viewed_id=user.id)
                db.session.add(v)
                db.session.commit()
        except:
            db.session.rollback()

    return render_template(
        "main/user_profile.html",
        user=user,
        profile=profile,
        conn=conn,
        posts=posts
    )
