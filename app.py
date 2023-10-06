from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
import csv

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route("/")
def home():
    with open("NLP_Dataset_Edits.csv", encoding="utf8") as file:
        reader = csv.reader(file)
        header = next(reader)
        return render_template("products.html", header=header, rows=reader)

@app.route("/search", methods = ['GET', 'POST'])
def search():
    return render_template("search.html")


if __name__ == '__main__':
    app.run(debug=True, port = 8000)