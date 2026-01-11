from . import campus_board_bp

from datetime import datetime, timedelta, timezone
from flask import request, jsonify, render_template
from flask_login import login_required, current_user

from extensions import db, csrf
from models import CampusBoardPost, CampusBoardLike
from factory_helpers import cleanup_expired_posts

from datetime import date
import json
from models import VibeQuestion, VibeResponse, VibeDailyState



#=============== Helper fucntions =================

# -------- vibe content to display ----
def get_vibe_context(user):
    today = date.today()
    question = VibeQuestion.query.filter_by(active_date=today).first()

    if not question:
        return {"mode": "inactive"}

    options = json.loads(question.options_json)

    response = VibeResponse.query.filter_by(
        question_id=question.id,
        user_id=user.id
    ).first()

    if not response:
        return {
            "mode": "input",
            "question": question,
            "options": options
        }

    state = VibeDailyState.query.get(today)

    return {
        "mode": "result",
        "question": question,
        "options": options,
        "state": state
    }





#=========== The routes =================

#main page of campus board
@campus_board_bp.route("/", methods=["GET"])
@login_required
def campus_board_page():
    vibe = get_vibe_context(current_user)
    return render_template(
        "campus_board/board.html",
        vibe=vibe
        )



#post creation
@campus_board_bp.route("/create", methods=["POST"])
@csrf.exempt
@login_required
def create_post():
    data = request.get_json()

    content = data.get("content", "").strip()
    if not content or len(content) > 300:
        return jsonify({"error": "Invalid content"}), 400

    department = data.get("department")
    location = data.get("location")

    expires_in_hours = data.get("expires_in_hours", 24)
    expires_in_hours = min(max(int(expires_in_hours), 1), 120)  # 5 days max

    post = CampusBoardPost(
        user_id=current_user.id,
        content=content,
        department=department,
        location=location,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=expires_in_hours)
    )

    db.session.add(post)
    db.session.commit()

    return jsonify({"success": True, "post_id": post.id})




#fetch active posts
@campus_board_bp.route("/list", methods=["GET"])
@csrf.exempt
@login_required
def list_posts():
    cleanup_expired_posts()
    now = datetime.now(timezone.utc)

    posts = (
        CampusBoardPost.query   
        .filter(CampusBoardPost.expires_at > now)
        .order_by(CampusBoardPost.expires_at.asc())
        .all()
    )

    return jsonify([
        {
            "id": p.id,
            "content": p.content,
            "department": p.department,
            "location": p.location,
            "expires_at": p.expires_at.isoformat(),
            "likes": p.likes_count,
            "is_owner": p.user_id == current_user.id
        }
        for p in posts
    ])



#liek the events 
@campus_board_bp.route("/like/<int:post_id>", methods=["POST"])
@csrf.exempt
@login_required
def toggle_like(post_id):
    post = CampusBoardPost.query.get_or_404(post_id)

    existing_like = CampusBoardLike.query.filter_by(
        campus_post_id=post.id,
        user_id=current_user.id
    ).first()

    if existing_like:
        db.session.delete(existing_like)
        post.likes_count = max(0, post.likes_count - 1)
        liked = False
    else:
        new_like = CampusBoardLike(
            campus_post_id=post.id,
            user_id=current_user.id
        )
        db.session.add(new_like)
        post.likes_count += 1
        liked = True

    db.session.commit()

    return jsonify({
        "success": True,
        "liked": liked,
        "likes": post.likes_count
    })





#delete own posts
@campus_board_bp.route("/delete/<int:post_id>", methods=["DELETE"])
@csrf.exempt
@login_required
def delete_post(post_id):
    post = CampusBoardPost.query.get_or_404(post_id)

    if post.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(post)
    db.session.commit()

    return jsonify({"success": True})
