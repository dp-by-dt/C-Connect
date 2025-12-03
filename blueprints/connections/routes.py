from . import connections  # blueprint
from flask import request, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from blueprints.connections.service import (
    send_connection_request,
    accept_connection,
    reject_connection,
    cancel_request,
    list_requests,
    list_connections,
    disconnect_connection
)
from blueprints.notifications.service import create_notification
from models import Connection
from extensions import db
from flask import jsonify

from extensions import limiter
from flask_limiter.util import get_remote_address



#---------- Helper functions
def get_connection_key():
    """Returns unique key: user123:target456"""
    return f"user:{current_user.id}:target:{request.view_args['target_id']}"

def get_user_key():
    """Returns user-only key for total limit"""
    return f"user:{current_user.id}"






# HOME PAGE — LIST CONNECTIONS
@connections.route('/connections')
@login_required
def connections_home():
    incoming = list_requests(current_user.id, 'incoming', 'pending', limit=50)
    outgoing = list_requests(current_user.id, 'outgoing', 'pending', limit=50)
    accepted = list_connections(current_user.id, limit=100)

    return render_template(
        'connections/list.html',
        incoming=incoming,
        outgoing=outgoing,
        accepted=accepted
    )



# SEND REQUEST
@connections.route('/connections/send/<int:target_id>', methods=['POST'])
@limiter.limit("3 per day", key_func=get_connection_key)  # Max 3/day to SAME person
@limiter.limit("25 per hour", key_func=lambda: f"user:{current_user.id}")  # 25 total/hour per user
@login_required
def connections_send(target_id):
    ok, msg, conn = send_connection_request(current_user.id, target_id)

    if ok:
        flash(msg, 'success')

        create_notification(
            user_id=target_id,
            sender_id=current_user.id,
            message=f"{current_user.username} sent you a connection request"
        )
    else:
        flash(msg, 'info')

    return redirect(request.referrer or url_for('main.home'))


# ACCEPT REQUEST
@connections.route('/connections/accept/<int:conn_id>', methods=['POST'])
@login_required
def connections_accept(conn_id):
    ok, msg, conn = accept_connection(conn_id, current_user.id)
    flash(msg, 'success' if ok else 'danger')

    if ok and conn:
        create_notification(
            user_id=conn.user_id,
            sender_id=current_user.id,
            message=f"{current_user.username} accepted your connection request"
        )

    return redirect(request.referrer or url_for('connections.connections_home'))


# REJECT REQUEST
@connections.route('/connections/reject/<int:conn_id>', methods=['POST'])
@login_required
def connections_reject(conn_id):
    ok, msg, conn = reject_connection(conn_id, current_user.id)
    flash(msg, 'info' if ok else 'danger')

    if ok and conn:
        create_notification(
            user_id=conn.user_id,
            sender_id=current_user.id,
            message=f"{current_user.username} rejected your connection request"
        )

    return redirect(request.referrer or url_for('connections.connections_home'))


# CANCEL SENT REQUEST
@connections.route('/connections/cancel/<int:conn_id>', methods=['POST'])
@login_required
def connections_cancel(conn_id):
    try:
        ok, msg, conn = cancel_request(conn_id, current_user.id)
        
        if ok and conn:
            create_notification(
                user_id=conn.target_user_id,
                sender_id=current_user.id,
                message=f"{current_user.username} cancelled their connection request"
            )
        
        # Return JSON - NO REDIRECT
        return jsonify({'ok': ok, 'message': msg})
    
    except Exception as e:
        app.logger.error(f"Cancel connection error: {str(e)}")
        return jsonify({'ok': False, 'message': 'Server error occurred'}), 500



# DISCONNECT AN EXISTING CONNECTION
@connections.route('/connections/disconnect/<int:conn_id>', methods=['POST'])
@login_required
def connections_disconnect(conn_id):
    ok, msg, conn = disconnect_connection(conn_id, current_user.id)
    flash(msg, 'success' if ok else 'danger')

    if ok and conn:
        # Determine the other user
        other_user = conn.target_user_id if conn.user_id == current_user.id else conn.user_id

        create_notification(
            user_id=other_user,
            sender_id=current_user.id,
            message=f"{current_user.username} removed you from their connections"
        )

    return redirect(request.referrer or url_for('connections.connections_home'))
