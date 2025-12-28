from . import messages
from flask import render_template, jsonify, flash, request
from flask_login import login_required, current_user
from models import User, Message, Connection, Notification
from flask import redirect, url_for
from extensions import db
from factory_helpers import cleanup_expired_messages
from datetime import datetime, timezone, timedelta
from sqlalchemy import desc

from blueprints.connections.service import is_connected




@messages.route("/")
@login_required
def inbox():
    cleanup_expired_messages()

    # 1. Get CONNECTED users
    connections = Connection.query.filter(
        Connection.user_id == current_user.id,
        Connection.status.in_(['accepted', 'connected'])
    ).all()

    incoming_connections = Connection.query.filter(
        Connection.target_user_id == current_user.id,
        Connection.status.in_(['accepted', 'connected'])
    ).all()

    connected_user_ids = set()
    for conn in connections + incoming_connections:
        other_id = conn.target_user_id if conn.user_id == current_user.id else conn.user_id
        connected_user_ids.add(other_id)

    connected_users = User.query.filter(User.id.in_(connected_user_ids)).all()



    # 2. Get INCOMING REQUESTS (pending)
    incoming_requests = Connection.query.filter(
        Connection.target_user_id == current_user.id,
        Connection.status == 'pending'
    ).all()

    incoming_users = User.query.filter(
        User.id.in_([req.user_id for req in incoming_requests])
    ).all()



    # 3. ULTRA SIMPLE - Get last message per user, sort properly
    chat_previews = {}
    messages = Message.query.filter(
        (Message.sender_id == current_user.id) |
        (Message.receiver_id == current_user.id)
    ).order_by(desc(Message.created_at)).all()

    seen_users = set()
    for msg in messages:
        other_id = msg.receiver_id if msg.sender_id == current_user.id else msg.sender_id
        if other_id in connected_user_ids and other_id not in seen_users:
            chat_previews[other_id] = msg  #  CORRECT last message
            seen_users.add(other_id)

    # SORT + PREVIEWS - most recent first
    connected_users_sorted = []
    for user_id in sorted(chat_previews.keys(), 
                        key=lambda x: chat_previews[x].created_at, reverse=True):
        user = User.query.get(user_id)
        if user:
            connected_users_sorted.append(user)

    # Add users with no chats at bottom (no preview)
    for user in connected_users:
        if user.id not in chat_previews:
            connected_users_sorted.append(user)

    connected_users = connected_users_sorted  


    return render_template("messages/inbox.html", 
                        connected_users=connected_users, 
                        incoming_requests=incoming_requests,
                        incoming_users=incoming_users,
                        chat_previews=chat_previews
                    )  





@messages.route("/<int:user_id>", methods=["GET", "POST"])
@login_required
def chat(user_id):
    cleanup_expired_messages()
    
    target_user = User.query.get_or_404(user_id)

    if request.method == "POST":
        
        # permission check for messaging
        if request.method == "POST":
            if not is_connected(current_user.id, user_id):
                flash("You can no longer send messages to this user.", "warning")
                return redirect(url_for("messages.chat", user_id=user_id))


        content = request.form.get("content", "").strip()
        if len(content) > 1000: #if the user chat is too lengthy
            flash("Message too long (max 1000 characters).", "error")
            return redirect(url_for("messages.chat", user_id=user_id))

        if content:
            msg = Message(
                sender_id=current_user.id,
                receiver_id=user_id,
                content=content,
                expires_at=datetime.now(timezone.utc) + timedelta(hours=24)
            )
            db.session.add(msg)
            db.session.commit()

            #send notificaiton to the other user
            if current_user.id != user_id:
                notif = Notification(
                    user_id=user_id,
                    sender_id=current_user.id,
                    message=f"New message from {current_user.username}",
                    type='message'
                )
                db.session.add(notif)

        return redirect(url_for("messages.chat", user_id=user_id))
    

    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.created_at.asc()).all()


    return render_template(
                "messages/chat.html", 
                messages=messages,
                target_user=target_user
            )
