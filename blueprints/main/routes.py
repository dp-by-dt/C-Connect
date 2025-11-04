from . import main
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
from models import User


# Home route - Landing page for guests, redirect for logged-in users
@main.route('/')
def home():
    # CHANGE: If user is logged in, redirect to dashboard (campus users go straight to dashboard)
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    
    # Otherwise, show landing page
    return render_template('main/home.html')


# About page
@main.route('/about')
def about():
    return render_template('main/about.html')


# Contact page
@main.route('/contact')
def contact():
    # CHANGE: Removed hardcoded name, can be dynamic later if needed
    return render_template('main/contact.html')


# NEW: Discover route - Browse all campus users
@main.route('/discover')
@login_required  # Only logged-in users can discover others
def discover():
    # Get search query from URL parameters (for future search functionality)
    search_query = request.args.get('search', '').strip()
    
    # Base query: All users except current user
    query = User.query.filter(User.id != current_user.id)
    
    # If search query exists, filter by username or email
    if search_query:
        query = query.filter(
            (User.username.ilike(f'%{search_query}%')) | 
            (User.email.ilike(f'%{search_query}%'))
        )
    
    # Fetch all matching users
    users = query.all()
    
    return render_template('main/discover.html', 
                         users=users, 
                         search_query=search_query)


# NEW: Messages placeholder route
@main.route('/messages')
@login_required
def messages():
    # Placeholder page for future messaging feature
    return render_template('main/messages.html')


# NEW: Search API endpoint (for AJAX calls - future use)
@main.route('/api/search_users')
@login_required
def search_users_api():
    """
    API endpoint for searching users dynamically.
    Returns JSON response for AJAX calls.
    Future use: Live search as user types.
    """
    search_query = request.args.get('q', '').strip()
    
    if not search_query or len(search_query) < 2:
        return jsonify({'users': []})
    
    # Search users by username or email
    users = User.query.filter(
        User.id != current_user.id,
        (User.username.ilike(f'%{search_query}%')) | 
        (User.email.ilike(f'%{search_query}%'))
    ).limit(10).all()
    
    # Convert to JSON-friendly format
    users_data = [
        {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
        for user in users
    ]
    
    return jsonify({'users': users_data})