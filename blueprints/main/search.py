# app/main/routes.py (add near other routes)
from flask import Blueprint, request, jsonify, render_template, current_app, url_for
from models import User, Profile, Connection
from sqlalchemy import or_, func, and_, String, cast
from app import db
from . import main


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
    # Renders search page template (with client-side fetch)
    query = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 12))
    if query:
        base = db.session.query(User).outerjoin(Profile).filter(search_filter(query))
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
        base = db.session.query(User).outerjoin(Profile).filter(search_filter(q)).filter(User.id != current_user.id) #Do not show current user ---- Might break if user not logged in
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
    status = "none"

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



        # render HTML snippet using the component (pass user & status)
        html_snippet = render_template('components/user_card.html', user=u, conn_status=status)


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





@main.route('/debug/search')
def debug_search():
    q = request.args.get('q', 'r').lower()
    users = db.session.query(User.username, Profile.department).outerjoin(Profile).filter(
        func.lower(func.coalesce(func.trim(User.username), '')).like(f"%{q}%")
    ).limit(10).all()
    
    # FIXED: users is list of tuples (username, department)
    return jsonify([{'username': row[0], 'dept': row[1]} for row in users])
