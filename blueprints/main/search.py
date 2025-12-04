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
    if not q: #no query, return empty
        return jsonify({'total':0,'results':[]})
    
    
    page = int(request.args.get('page', 1))
    per_page = min(int(request.args.get('per_page', 12)), 50)

    base = (
        db.session.query(User)
        .join(Profile)
        .filter(fuzzy_query(q))
        .filter(User.id != current_user.id)#Do not show current user ---- Might break if user not logged in
    )
    total = base.count()
    users = base.order_by(User.last_login.desc()).limit(per_page).offset((page-1)*per_page).all()


    conn = Connection.query.filter(
        (
            (Connection.user_id == current_user.id) &
            (Connection.target_user_id == u.id)
        ) |
        (
            (Connection.user_id == u.id) &
            (Connection.target_user_id == current_user.id)
        )
    ).first()

    connection_status = conn.status if conn else None
    incoming_request = (conn and conn.target_user_id == current_user.id and conn.status == 'pending')
    connection_id = conn.id if conn else None


    out = []
    for u in users:
        out.append({
            'id': u.id,
            'name': u.username,
            'bio': u.profile.bio or '',
            'department': u.profile.department or '',
            'avatar_url': url_for('static', filename='uploads/avatars/' + (u.profile.profile_picture or 'default.png')),
            'mutuals': u.mutual_count if hasattr(u,'mutual_count') else 0
        })
    return jsonify({'total': total, 
                    'results': out, 'page': page, 
                    'per_page': per_page,
                    'connection_status': connection_status,
                    'incoming_request': incoming_request,
                    'connection_id': connection_id,
                    })
