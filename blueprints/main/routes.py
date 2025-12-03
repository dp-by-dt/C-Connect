from . import main
from flask import render_template
from flask_login import login_required, current_user
from models import User, Profile  # For user discovery feature
from models import Connection, ProfileVisit  # For viewing other user's profile
from flask import redirect, url_for
from extensions import db
from flask import abort
from flask import request

from sqlalchemy import case

from datetime import datetime, timezone



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

    return render_template('main/dashboard.html', username=current_user.username, stats=stats)




# NEW ROUTE: User discovery page
# REASON: Core feature for social network; allows users to find and connect with others
@main.route('/discover')
@login_required
def discover():
    # Fetch all users except the current user
    # Quick offset pagination
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 12, type=int), 50)

    query = User.query.outerjoin(Profile).filter(User.id != current_user.id)
    total = query.count()
    max_page = (total + per_page - 1) // per_page  # Calculate last page

    # REDIRECT INVALID PAGES
    if page < 1:
        return redirect(url_for('main.discover', page=1))
    if page > max_page and total > 0:
        return redirect(url_for('main.discover', page=max_page))


    # COALESCE - Active FIRST, Inactive AFTER!
    users = (query
             .order_by(
                 case(
                     (User.last_login.is_(None), 1),  # NULL = 1 (last)
                     else_=0  # NOT NULL = 0 (first)
                 ),
                 User.last_login.desc(),  # Recent first
                 User.id  # Tiebreaker
             )
             .offset((page-1)*per_page)
             .limit(per_page)
             .all())
    

    has_next = page*per_page < total
    return render_template('main/discover.html', 
                         users=users, 
                         page=page, 
                         per_page=per_page, 
                         has_next=has_next,
                         total=total)



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
        conn=conn
    )
