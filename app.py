from flask import Flask, render_template


app = Flask(__name__)

#render the base html template
@app.route('/')
def base():
    return render_template('base.html')


#make the buttons work to go to the respective webpages
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact(var_name="Jennifer"):
    return render_template('contact.html',name=var_name)


if __name__ == '__main__':
    app.run(debug=True)