from models import User # Importing User model for querying


#Testing the db
@app.route('/show_users')
def show_users():
    users = User.query.all()  # Fetch all users
    arr = [(user.id, user.username, user.email, user.password) for user in users]
    if not arr:
        return 'No users found'
    return '<br>'.join([f'Id {id}, Username: {username}, Email: {email}, Pass: {password}' for id, username, email, password in arr])