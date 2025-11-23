from extensions import db
from models import Notification
from datetime import datetime, timedelta, timezone
from flask import current_app

def create_notification(user_id, sender_id, message):
    notif = Notification(
        user_id=user_id,
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

