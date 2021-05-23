from flask import Flask, escape, request, render_template
from Air_Canvas_HTR import AirCanvas
import pickle

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        inf = AirCanvas()
        return render_template("result.html",result = inf)         
    return render_template("index.html")
@app.route('/contact')
def contact():
    return render_template("contact.html")
@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run('localhost', 8000, debug=True)

