from . import messages
from flask import render_template, jsonify, flash, request
from flask_login import login_required, current_user
from models import User, Message, Connection
from flask import redirect, url_for
from extensions import db
from factory_helpers import cleanup_expired_messages
from datetime import datetime, timezone, timedelta

from blueprints.connections.service import is_connected




@messages.route("/")
@login_required
def inbox():
    cleanup_expired_messages()

    # users you have chatted with
    messages = Message.query.filter(
        (Message.sender_id == current_user.id) |
        (Message.receiver_id == current_user.id)
    ).order_by(Message.created_at.desc()).all()

    chat_users = {}
    for msg in messages:
        other_id = msg.receiver_id if msg.sender_id == current_user.id else msg.sender_id
        chat_users[other_id] = msg

    users = User.query.filter(User.id.in_(chat_users.keys())).all()

    return render_template("messages/inbox.html", users=users)




@messages.route("/<int:user_id>", methods=["GET", "POST"])
@login_required
def chat(user_id):
    cleanup_expired_messages()

    # permission check
    if not is_connected(current_user.id, user_id):
        flash("You can only message connected users", "error")
        return redirect(url_for("messages.inbox"))

    if request.method == "POST":
        content = request.form.get("content", "").strip()
        if content:
            msg = Message(
                sender_id=current_user.id,
                receiver_id=user_id,
                content=content,
                expires_at=datetime.utcnow() + timedelta(hours=24)
            )
            db.session.add(msg)
            db.session.commit()
        return redirect(url_for("messages.chat", user_id=user_id))

    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.created_at.asc()).all()

    return render_template("messages/chat.html", messages=messages)
