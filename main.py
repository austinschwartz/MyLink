from flask import Flask, render_template

app = Flask(__name__)

fakeuser = {'email':'bob@yahoo.com', 'password':'hunter2'}

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html', user=fakeuser);

@app.route("/login")
def login():
    return render_template('login.html', title='Login');

if __name__ == "__main__":
    app.run(port = 8080, debug = True)
