from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route("/")
def home():
    return render_template("products.html")

@app.route("/search", methods = ['GET', 'POST'])
def search():
    return render_template("search.html")


if __name__ == '__main__':
    app.run(debug=True, port = 8000)