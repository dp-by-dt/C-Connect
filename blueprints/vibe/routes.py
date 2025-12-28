import json
import random
from datetime import date, datetime, timezone

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from extensions import db
from . import vibe_bp
from models import (
    VibeQuestion,
    VibeResponse,
    VibeReport,
    VibeDailyState
)



# ----- helper functions -----------------

def get_or_create_today_question():
    today = date.today()

    question = VibeQuestion.query.filter_by(active_date=today).first()
    if question:
        return question

    # 🔹 v1 default question (can rotate later)
    options = ["Easy", "Meh", "Disaster"]

    question = VibeQuestion(
        question_text="How bad was today's exam?",
        options_json=json.dumps(options),
        active_date=today
    )

    db.session.add(question)
    db.session.commit()
    return question


def has_user_voted(question_id):
    return VibeResponse.query.filter_by(
        question_id=question_id,
        user_id=current_user.id
    ).first()



def update_daily_state(question):
    today = question.active_date

    responses = (
        VibeResponse.query
        .filter_by(question_id=question.id)
        .all()
    )

    if not responses:
        return

    counts = {}
    for r in responses:
        counts[r.choice_index] = counts.get(r.choice_index, 0) + 1

    dominant_choice = max(counts, key=counts.get)

    # 🎨 simple color mapping (v1)
    color_map = {
        0: "#4CAF50",  # green
        1: "#FFC107",  # amber
        2: "#F44336",  # red
        3: "#9C27B0",  # purple (future)
        4: "#2196F3",  # blue (future)
    }

    state = VibeDailyState.query.get(today)
    if not state:
        state = VibeDailyState(date=today)

    state.total_responses = len(responses)
    state.dominant_choice = dominant_choice
    state.accent_color = color_map.get(dominant_choice, "#2196F3")

    db.session.add(state)
    db.session.commit()





# -------- Routes --------------
@vibe_bp.route("/")
@login_required
def daily_vibe():
    question = get_or_create_today_question()
    options = json.loads(question.options_json)

    user_response = has_user_voted(question.id)

    # 🚪 INPUT VIEW (locked)
    if not user_response:
        return render_template(
            "vibe/daily_vibe.html",
            mode="input",
            question=question,
            options=options
        )

    # 📊 RESULT VIEW
    state = VibeDailyState.query.get(question.active_date)

    # Ghost Tape: last 100 → sample 20
    recent_lines = (
        VibeResponse.query
        .filter(
            VibeResponse.question_id == question.id,
            VibeResponse.is_hidden.is_(False),
            VibeResponse.anonymous_text.isnot(None)
        )
        .order_by(VibeResponse.created_at.desc())
        .limit(100)
        .all()
    )

    ghost_tape = random.sample(
        recent_lines,
        min(len(recent_lines), 20)
    )

    return render_template(
        "vibe/daily_vibe.html",
        mode="result",
        question=question,
        options=options,
        state=state,
        ghost_tape=ghost_tape
    )


@vibe_bp.route("/respond", methods=["POST"])
@login_required
def respond_vibe():
    question = get_or_create_today_question()

    # Prevent double vote
    if has_user_voted(question.id):
        flash("You have already responded today.", "warning")
        return redirect(url_for("vibe.daily_vibe"))

    try:
        choice_index = int(request.form.get("choice"))
    except (TypeError, ValueError):
        flash("Invalid response.", "error")
        return redirect(url_for("vibe.daily_vibe"))

    options = json.loads(question.options_json)
    if choice_index < 0 or choice_index >= len(options):
        flash("Invalid option selected.", "error")
        return redirect(url_for("vibe.daily_vibe"))

    text = request.form.get("anonymous_text", "").strip()
    if text and len(text) > 80:
        flash("Text too long (max 80 characters).", "error")
        return redirect(url_for("vibe.daily_vibe"))

    response = VibeResponse(
        question_id=question.id,
        user_id=current_user.id,
        choice_index=choice_index,
        anonymous_text=text or None
    )

    db.session.add(response)
    db.session.commit()

    update_daily_state(question)

    return redirect(url_for("vibe.daily_vibe"))




@vibe_bp.route("/vanish/<int:response_id>", methods=["POST"])
@login_required
def vanish_response(response_id):
    response = VibeResponse.query.get_or_404(response_id)

    # Prevent self-vanish
    if response.user_id == current_user.id:
        return redirect(url_for("vibe.daily_vibe"))

    # Check if already reported by this user
    existing = VibeReport.query.filter_by(
        response_id=response_id,
        user_id=current_user.id
    ).first()

    if existing:
        return redirect(url_for("vibe.daily_vibe"))

    report = VibeReport(
        response_id=response_id,
        user_id=current_user.id
    )

    response.vanish_count += 1

    # 🚨 Threshold = 3
    if response.vanish_count >= 3:
        response.is_hidden = True

    db.session.add(report)
    db.session.commit()

    return redirect(url_for("vibe.daily_vibe"))



