# blueprints/connections/routes.py
from . import connections  # blueprint
from flask import request, redirect, url_for, flash, jsonify, render_template
from flask_login import login_required, current_user
from blueprints.connections.service import send_connection_request, accept_connection, reject_connection, cancel_request, list_requests, list_connections



@connections.route('/connections')
@login_required
def connections_home():
    incoming = list_requests(current_user.id, 'incoming', 'pending', limit=50)
    outgoing = list_requests(current_user.id, 'outgoing', 'pending', limit=50)
    accepted = list_connections(current_user.id, limit=100)
    return render_template('connections/list.html', incoming=incoming, outgoing=outgoing, accepted=accepted)


@connections.route('/connections/send/<int:target_id>', methods=['POST'])
@login_required
def connections_send(target_id):
    ok, msg, obj = send_connection_request(current_user.id, target_id)
    if ok:
        flash(msg, 'success')
    else:
        flash(msg, 'info')
    return redirect(request.referrer or url_for('main.home'))


@connections.route('/connections/accept/<int:conn_id>', methods=['POST'])
@login_required
def connections_accept(conn_id):
    ok, msg, obj = accept_connection(conn_id, current_user.id)
    flash(msg, 'success' if ok else 'danger')
    return redirect(request.referrer or url_for('connections.connections_home'))


@connections.route('/connections/reject/<int:conn_id>', methods=['POST'])
@login_required
def connections_reject(conn_id):
    ok, msg, obj = reject_connection(conn_id, current_user.id)
    flash(msg, 'info' if ok else 'danger')
    return redirect(request.referrer or url_for('connections.connections_home'))


@connections.route('/connections/cancel/<int:conn_id>', methods=['POST'])
@login_required
def connections_cancel(conn_id):
    ok, msg = cancel_request(conn_id, current_user.id)
    flash(msg, 'info' if ok else 'danger')
    return redirect(request.referrer or url_for('connections.connections_home'))


@connections.route("/connections")
@login_required
def connections_list():
    # service methods handle logic cleanly
    incoming = list_requests(current_user.id, "incoming")
    outgoing = list_requests(current_user.id, "outgoing")
    accepted = list_connections(current_user.id)

    return render_template("connections/list.html",
        incoming=incoming, outgoing=outgoing, accepted=accepted)
