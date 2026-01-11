from . import notifications
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for
from models import Notification
from extensions import db
from flask import flash

@notifications.route('/notifications_list')
@login_required
def notifications_list():
    notifs = Notification.query.filter_by(user_id=current_user.id) \
                .order_by(Notification.created_at.desc()) \
                .all()

    return render_template('notifications/notif_list.html', notifs=notifs)




@notifications.route('/mark/<int:notif_id>')
@login_required
def mark_read(notif_id):
    notif = Notification.query.get_or_404(notif_id)
    if notif.user_id != current_user.id:
        return "Unauthorized", 403

    notif.is_read = True
    db.session.commit()

    # campus daily notification → go to campus board
    if notif.type == "campus_daily":
        return redirect(url_for("campus_board_bp.campus_board_page"))
    
    return redirect(url_for('notifications.notifications_list'))



@notifications.route('/notifications/mark_all_read', methods=['POST'])
@login_required
def mark_all_read():
    Notification.query.filter_by(user_id=current_user.id, is_read=False).update(
        {Notification.is_read: True}
    )
    db.session.commit()
    flash("Notifications marked as read.", "info")
    return redirect(url_for('notifications.notifications_list'))
