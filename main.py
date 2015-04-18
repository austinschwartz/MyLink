from flask import Flask, render_template
import jinja2
import os

app = Flask(__name__)
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader("templates"),autoescape=True)

@app.route("/")
def main():
    return render_template('login.html');

if __name__ == "__main__":
    app.run(port = 8080, debug = True)
