from flask import Flask, render_template, session, redirect, url_for, escape, request

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html', user = session['username'])

@app.route('/user/<username>')
def profile():
    return

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html', title='Login')

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(port = 8080, debug = True)
