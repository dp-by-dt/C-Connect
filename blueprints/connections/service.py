# blueprints/connections/service.py
from sqlalchemy.exc import IntegrityError
from extensions import db
from models import Connection, User
from datetime import datetime

VALID_STATUSES = {"pending", "accepted", "rejected", "blocked"}

def send_connection_request(sender_id: int, target_id: int):
    """Return (success, message, connection_or_none)."""
    if sender_id == target_id:
        return False, "Cannot connect to yourself.", None

    # Prevent repeated requests in either direction if already accepted
    existing = Connection.query.filter(
        ((Connection.user_id == sender_id) & (Connection.target_user_id == target_id)) |
        ((Connection.user_id == target_id) & (Connection.target_user_id == sender_id))
    ).first()

    if existing:
        if existing.status == 'pending' and existing.user_id == sender_id:
            return False, "Request already sent.", existing
        if existing.status == 'pending' and existing.user_id == target_id:
            return False, "They have already sent you a request.", existing
        if existing.status == 'accepted':
            return False, "You are already connected.", existing
        if existing.status == 'blocked':
            return False, "Connection blocked.", existing
        # if rejected earlier, maybe allow re-send — choose policy:
        # We'll allow re-sending after rejection:
        if existing.status == 'rejected' and existing.user_id == sender_id:
            # re-create / update to pending
            existing.status = 'pending'
            existing.created_at = db.func.now()
            try:
                db.session.commit()
                return True, "Request re-sent.", existing
            except Exception as e:
                db.session.rollback()
                raise

    # No existing request, create one
    new_conn = Connection(user_id=sender_id, target_user_id=target_id, status='pending')
    db.session.add(new_conn)
    try:
        db.session.commit()
        return True, "Request sent.", new_conn
    except IntegrityError as ie:
        db.session.rollback()
        # possibly duplicate insert raced in
        existing = Connection.query.filter_by(user_id=sender_id, target_user_id=target_id).first()
        if existing:
            return False, "Request already exists.", existing
        raise
    except Exception:
        db.session.rollback()
        raise


def accept_connection(conn_id: int, receiver_id: int):
    """Receiver accepts a pending connection."""
    conn = Connection.query.get(conn_id)
    if not conn:
        return False, "Request not found.", None
    if conn.target_user_id != receiver_id:
        return False, "Not authorized to accept.", None
    if conn.status != 'pending':
        return False, f"Cannot accept a request with status {conn.status}.", conn

    conn.status = 'accepted'
    conn.created_at = db.func.now()  # optionally update
    try:
        db.session.commit()
        return True, "Request accepted.", conn
    except Exception:
        db.session.rollback()
        raise


def reject_connection(conn_id: int, receiver_id: int):
    conn = Connection.query.get(conn_id)
    if not conn:
        return False, "Request not found.", None
    if conn.target_user_id != receiver_id:
        return False, "Not authorized to reject.", None
    if conn.status != 'pending':
        return False, f"Cannot reject a request with status {conn.status}.", conn

    conn.status = 'rejected'
    try:
        db.session.commit()
        return True, "Request rejected.", conn
    except Exception:
        db.session.rollback()
        raise


def cancel_request(conn_id: int, sender_id: int):
    conn = Connection.query.get(conn_id)
    if not conn:
        return False, "Request not found.", conn
    if conn.user_id != sender_id:
        return False, "Not authorized to cancel.", conn
    if conn.status != 'pending':
        return False, "Only pending requests can be cancelled.", conn
    try:
        db.session.delete(conn)
        db.session.commit()
        return True, "Request cancelled.", conn
    except Exception:
        db.session.rollback()
        raise


def list_requests(user_id: int, direction='incoming', status='pending', limit=50, offset=0):
    """Return incoming/outgoing connections filtered by status."""
    q = Connection.query
    if direction == 'incoming':
        q = q.filter_by(target_user_id=user_id)
    else:
        q = q.filter_by(user_id=user_id)
    if status:
        q = q.filter_by(status=status)
    q = q.order_by(Connection.created_at.desc()).limit(limit).offset(offset)
    return q.all()


def list_connections(user_id: int, limit=50, offset=0):
    q = Connection.query.filter(
        (Connection.status == 'accepted') & (
            (Connection.user_id == user_id) | (Connection.target_user_id == user_id)
        )
    ).order_by(Connection.created_at.desc()).limit(limit).offset(offset)
    return q.all()


def is_connected(user_a: int, user_b: int):
    c = Connection.query.filter(
        ((Connection.user_id == user_a) & (Connection.target_user_id == user_b)) |
        ((Connection.user_id == user_b) & (Connection.target_user_id == user_a))
    ).filter_by(status='accepted').first()
    return bool(c)



# service.py
def disconnect_connection(conn_id: int, user_id: int):
    """
    Disconnect an accepted connection. Only participants may disconnect.
    Returns (ok:bool, msg:str)
    """
    conn = Connection.query.get(conn_id)
    if not conn:
        return False, "Connection not found.", conn

    # Verify user is one of the participants
    if user_id not in (conn.user_id, conn.target_user_id):
        return False, "Not authorized to disconnect.", conn

    # If not accepted, you probably want to allow deletion of pending too, but we restrict to accepted
    if conn.status != 'accepted':
        # allow cancel if it's your pending request
        if conn.status == 'pending' and conn.user_id == user_id:
            try:
                db.session.delete(conn)
                db.session.commit()
                return True, "Pending request cancelled.", conn
            except Exception:
                db.session.rollback()
                raise
        return False, f"Cannot disconnect connection with status '{conn.status}'.", conn

    try:
        db.session.delete(conn)
        db.session.commit()
        return True, "Disconnected successfully.", conn
    except Exception:
        db.session.rollback()
        raise
