# app/main/routes.py (add near other routes)
from flask import Blueprint, request, jsonify, render_template, current_app, url_for
from models import User, Profile, Connection
from sqlalchemy import or_, func, and_, String, cast, distinct
from app import db
from . import main
from sqlalchemy.orm import joinedload



from flask_login import login_required, current_user




def search_filter(q):
    q = q.lower().strip()
    
    # BULLETPROOF username search
    username_match = func.lower(func.coalesce(func.trim(User.username), '')).like(f"%{q}%")
    
    #bio_text = func.lower(func.coalesce(cast(Profile.bio, String), ""))
    dept_text = func.lower(func.coalesce(cast(Profile.department, String), ""))
    year_text = func.lower(func.coalesce(cast(Profile.year, String), ""))
    
    if len(q) < 3:
        return username_match
    return or_(
        username_match,
        #bio_text.like(f"%{q}%"),
        #dept_text.like(f"%{q}%"),
        #year_text.like(f"%{q}%"),
        #right now only trying to search on the username, other will be added as a filter
    )


@main.route('/search')
@login_required
def search_page():
    query = request.args.get('q', '')
    return render_template('main/search.html', query=query)




@main.route('/api/search')
@login_required
def api_search():
    q = request.args.get('q', '').strip()
    offset = int(request.args.get('offset', 0))
    limit = min(int(request.args.get('limit', 20)), 50)

    base = (
        db.session.query(User)
        .options(joinedload(User.profile))
        .filter(User.id != current_user.id)
    )

    if q:
        base = base.filter(search_filter(q))

    base = base.order_by(
        User.last_login.desc().nullslast(),
        User.id.desc()
    )

    users = base.offset(offset).limit(limit).all()

    # END CONDITION — CRITICAL
    if not users:
        return jsonify({
            "results": [],
            "has_more": False
        })

    results = []

    for u in users:
        status = "none"

        conn = Connection.query.filter(
            ((Connection.user_id == current_user.id) &
             (Connection.target_user_id == u.id)) |
            ((Connection.user_id == u.id) &
             (Connection.target_user_id == current_user.id))
        ).first()

        if conn:
            if conn.status in ("accepted", "connected"):
                status = "connected"
            elif conn.status == "pending":
                if conn.user_id == current_user.id:
                    status = "requested"    # You sent the request
                elif conn.target_user_id == current_user.id:
                    status = "incoming"     # They sent you a request
            else:
                status = "unknown"

        html = render_template(
            "components/user_card.html",
            user=u,
            conn_status=status
        )

        results.append({"html": html})

    return jsonify({
        "results": results,
        "has_more": len(results) == limit
    })



@main.route('/debug/search')
def debug_search():
    q = request.args.get('q', 'r').lower()
    users = db.session.query(User.username, Profile.department).outerjoin(Profile).filter(
        func.lower(func.coalesce(func.trim(User.username), '')).like(f"%{q}%")
    ).limit(10).all()
    
    # FIXED: users is list of tuples (username, department)
    return jsonify([{'username': row[0], 'dept': row[1]} for row in users])
