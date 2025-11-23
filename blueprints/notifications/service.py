from extensions import db
from models import Notification

def create_notification(user_id, sender_id, message):
    notif = Notification(
        user_id=user_id,
        sender_id=sender_id,
        message=message
    )
    db.session.add(notif)
    db.session.commit()
    return notif
