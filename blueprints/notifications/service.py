from extensions import db
from models import Notification, CampusBoardPost
from datetime import datetime, timedelta, timezone, date
from flask import current_app


#notification for connections
def create_notification(user_id, sender_id, message):
    notif = Notification(
        user_id=user_id,
        type='connect',
        sender_id=sender_id,
        message=message
    )
    db.session.add(notif)
    db.session.commit()
    return notif



#auto delete notifications older than 24 hours
def cleanup_old_notifications():
    expiry_hours = current_app.config.get("NOTIFICATION_EXPIRY_HOURS", 24)
    cutoff = datetime.now(timezone.utc) - timedelta(hours=expiry_hours)

    old = Notification.query.filter(Notification.created_at < cutoff).all()
    count = len(old)

    for n in old:
        db.session.delete(n)

    if count > 0:
        db.session.commit()

    return count




# ----------- Notification for campus board event ----------
def create_daily_campus_notification_for_user(user):
    """
    Create one campus notification per user per day
    if there is at least one active campus board post.
    """

    today = date.today()

    # 1. Check if user already has today's campus notification
    existing = Notification.query.filter(
        Notification.user_id == user.id,
        Notification.type == "campus_daily",
        Notification.created_at >= datetime.combine(today, datetime.min.time(), tzinfo=timezone.utc)
    ).first()

    if existing:
        return False  # already created

    # 2. Check if there is at least one active campus board post
    now = datetime.now(timezone.utc)
    active_exists = CampusBoardPost.query.filter(
        CampusBoardPost.expires_at > now
    ).first()

    if not active_exists:
        return False  # nothing to notify about

    # 3. Create notification
    notif = Notification(
        user_id=user.id,
        type="campus_daily_event",
        message="New campus updates available",
        ref_id=None
    )

    db.session.add(notif)
    db.session.commit()
    return True
