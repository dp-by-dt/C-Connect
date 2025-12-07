# app/main/routes.py (add near other routes)
from flask import Blueprint, request, jsonify, render_template, current_app, url_for
from models import User, Profile, Connection
from sqlalchemy import or_, func, and_
from app import db
from . import main

from flask_login import login_required, current_user



def fuzzy_query(q):
    pattern = f"%{q.lower()}%"
    return or_(
        func.lower(User.username).like(pattern),
        func.lower(Profile.bio).like(pattern),
        func.lower(Profile.department).like(pattern),
        func.lower(Profile.year).like(pattern)
    )

@main.route('/search')
def search_page():
    # Renders search page template (with client-side fetch)
    query = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 12))
    if query:
        base = db.session.query(User).join(Profile).filter(fuzzy_query(query))
        total = base.count()
        items = base.order_by(User.last_login.desc()).limit(per_page).offset((page-1)*per_page).all()
    else:
        total = 0
        items = []
    # Template will request via AJAX too; we return initial render
    return render_template('main/search.html', 
                           query=query, results=items, total=total, page=page, per_page=per_page,
                           )



@main.route('/api/search')
@login_required
def api_search():
    q = request.args.get('q', '').strip()

    page = int(request.args.get('page', 1))
    per_page = min(int(request.args.get('per_page', 12)), 50)

    if q:
        base = db.session.query(User).outerjoin(Profile).filter(fuzzy_query(q)).filter(User.id != current_user.id) #Do not show current user ---- Might break if user not logged in
    else:
        # no query → return recent active users (same logic as discover)
        base = db.session.query(User).outerjoin(Profile).filter(User.id != current_user.id)
        # order by last_login desc (recent first)
        base = base.order_by(User.last_login.desc())



    total = base.count()
    users = (base
             .order_by(User.last_login.desc())
             .limit(per_page)
             .offset((page-1)*per_page)
             .all())


    results = []
    for u in users:

        # Determine connection relationship with current_user and u
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
                # If current user RECEIVED the request
                if conn.target_user_id == current_user.id:
                    status = "incoming"
                else:
                    status = "pending"
        else:
            status = "none"


        # render HTML snippet using the component (pass user & status)
        html_snippet = render_template('components/user_card.html',
                                     user=u, conn_status=status,
                                     **request.args.to_dict())  # Pass query params


        results.append({
            'id': u.id,
            'name': u.username,
            #'bio': u.profile.bio,
            'department': (u.profile.department if u.profile else None),
            'avatar_url': url_for('static',
               filename='uploads/' + (u.profile.profile_picture or 'default.png')) if u.profile else url_for('static',filename='images/avatar-placeholder.jpg'),
            'connection_status': status,
            #'mutuals': u.mutual_count if hasattr(u,'mutual_count') else 0,
            'html':html_snippet
        })

    return jsonify({
        'total': total,
        'page': page,
        'per_page': per_page,
        'results': results
    })



