from flask import Flask, render_template, url_for, request
from flask_bootstrap import Bootstrap
import pandas as pd

import csv

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route("/")
def home():
        return render_template("index.html")

@app.route("/products")
def products():
     with open("NLP_Dataset_Edits.csv", encoding="utf8") as file:
        reader = csv.reader(file)
        header = next(reader)
        return render_template("products.html", header=header, rows=reader)


@app.route("/search", methods=["POST", "GET"] )
def search():
    if request.method == 'POST':
        search_query = request.form.get('dataresult')
        results = []
        data = pd.read_pickle('NLP_Dataset.pkl')
        print(search_query)
        for index in data.index:
            product_name = data['Product'][index]
            if search_query.lower() in product_name.lower():
                results.append(data.iloc[index])
                
        lengthlist= len(results)
        print(results)
        print(lengthlist)
    return render_template("search.html", results = results, lengthlist=lengthlist)


if __name__ == '__main__':
    app.run(debug=True, port = 8000)