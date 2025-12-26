#=========== TEMPLATE FOR THE ADDITION ===========
'''
REMOVED FROM:
REMOVED BECAUSE:
GITHUB COMMIT AFTER REMOVAL:
OTHER CHANGED DID WHILE REMOVING:
NOTE:

------------------
CONTENT(don't forget to comment out; for safety):

'''



#---------- discover removal
'''
REMOVED FROM: blueprints/main/routes.py
REMOVED BECAUSE: /discover no longer needed. Replaced now by the route /search
GITHUB COMMIT AFTER REMOVAL: "Day 13.7: Discover replaced by search"
OTHER CHANGED DID WHILE REMOVING: created this 'removed.py' file, replaced the discover link from nav to search (but name is still discover)
NOTE: The routes '/discover' and '/api/discover' were removed

------------------
CONTENT(don't forget to comment out; for safety):


    # NEW ROUTE: User discovery page
    # REASON: Core feature for social network; allows users to find and connect with others
    @main.route('/discover')
    @login_required
    def discover(): #uses pagination (for web pages)
        # Fetch all users except the current user
        # Quick offset pagination
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 12, type=int), 50)

        query = User.query.outerjoin(Profile).filter(User.id != current_user.id)
        total = query.count()
        max_page = (total + per_page - 1) // per_page  # Calculate last page

        # REDIRECT INVALID PAGES
        if page < 1:
            return redirect(url_for('main.discover', page=1))
        if page > max_page and total > 0:
            return redirect(url_for('main.discover', page=max_page))


        # COALESCE - Active FIRST, Inactive AFTER!
        users = (query
                .order_by(
                    case(
                        (User.last_login.is_(None), 1),  # NULL = 1 (last)
                        else_=0  # NOT NULL = 0 (first)
                    ),
                    User.last_login.desc(),  # Recent first
                    User.id  # Tiebreaker
                )
                .offset((page-1)*per_page)
                .limit(per_page)
                .all())
        

        #return user's connection status
        users_data = []
        for user in users:
            # DYNAMIC STATUS CHECK
            conn_status = get_connection_status(current_user.id, user.id)
            users_data.append({
                'user': user,
                'conn_status': conn_status
            })
        

        has_next = page*per_page < total
        return render_template('main/discover.html', 
                            users=users_data, 
                            page=page, 
                            per_page=per_page, 
                            has_next=has_next,
                            total=total)


    #Uses cursor for infinite scrolling
    @main.route('/api/discover')  # Mobile - Infinite scroll
    @login_required
    def api_discover():
        # Cursor pagination
        def parse_cursor(cur):
            # example: "2025-12-03T14:33:00|123"
            ts_str, id_str = cur.split("|")
            ts = datetime.fromisoformat(ts_str)
            id = int(id_str)
            return ts, id

        limit = min(int(request.args.get('limit',20)), 50)
        cursor = request.args.get('cursor', None)
        q = User.query.join(Profile).filter(User.id != current_user.id)

        if cursor:
            last_ts, last_id = parse_cursor(cursor)
            # keyset: (last_login, id) descending
            q = q.filter(
                or_(
                    User.last_login < last_ts,
                    and_(User.last_login == last_ts, User.id < last_id)
                )
            )

        q = q.order_by(User.last_login.desc(), User.id.desc()).limit(limit + 1)
        items = q.all()
        has_more = len(items) == limit + 1
        page_items = items[:limit]
        next_cursor = None
        if has_more:
            last = items[-2]  # last real item
            next_cursor = f"{last.last_login.isoformat()}|{last.id}"

        return jsonify({
            'users': [user.to_dict() for user in page_items],
            'next_cursor': next_cursor
        })

'''