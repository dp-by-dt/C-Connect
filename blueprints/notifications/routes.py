from . import notifications
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for
from models import Notification
from extensions import db


@notifications.route('/notifications_list')
@login_required
def notifications_list():
    notifs = Notification.query.filter_by(user_id=current_user.id) \
                .order_by(Notification.created_at.desc()) \
                .all()
    
    # Mark unread as read when viewed
    #only want to do this, once the user views it and goes back (later)
    for notif in notifs:
        if not notif.is_read:
            notif.is_read = True

    db.session.commit()


    return render_template('notifications/notif_list.html', notifs=notifs)




@notifications.route('/mark/<int:notif_id>')
@login_required
def mark_read(notif_id):
    notif = Notification.query.get_or_404(notif_id)
    if notif.user_id != current_user.id:
        return "Unauthorized", 403

    notif.is_read = True
    db.session.commit()
    return redirect(url_for('notifications.notifications_list'))

@notifications.route('/mark_all')
@login_required
def mark_all_read():
    Notification.query.filter_by(user_id=current_user.id, is_read=False).update({"is_read": True})
    db.session.commit()
    return redirect(url_for('notifications.notifications_list'))
