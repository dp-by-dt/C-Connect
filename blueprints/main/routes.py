from . import main
from flask import render_template


# route to the main page
@main.route('/')
def home():
    return render_template('base.html')




# route to about and contact pages ----------

@main.route('/about')
def about():
    return render_template('main/about.html')

@main.route('/contact')
def contact():
    return render_template('main/contact.html', name='Someone1')
