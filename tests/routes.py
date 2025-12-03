
from flask import redirect, url_for
from flask import flash


@app.route('/test')
def test_flash():
    flash('Success! Flash working.', 'success')
    flash('Error example.', 'danger')
    return redirect(url_for('main.home'))
