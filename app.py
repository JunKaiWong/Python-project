from flask import Flask, render_template, url_for, request, Response, send_file, redirect
from flask_bootstrap import Bootstrap
import pandas as pd
from bs4 import BeautifulSoup
import csv

app = Flask(__name__)
bootstrap = Bootstrap(app)

filteredsorted_results = []


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

    global filteredsorted_results

    if request.method == 'POST':
        search_query = request.form.get('dataresult')    
        searchresults = []
        sorted_results=[]
        count = 0
        data = pd.read_csv('NLP_Dataset_Cut (1).csv')     

        for index in data.index:
            product_name = data['Product'][index].replace("/", " ")
            if search_query.lower() in product_name.lower():
                searchresults.append(data.iloc[index])
                # sorted_results = sorted(searchresults, key = lambda x: x['Stars'], reverse=True)
                count +=1
            
        sorted_results = sorted(searchresults, key = lambda x: x['Stars'], reverse=True)

        if len(sorted_results) >= 50:
            filteredsorted_results = sorted_results[:51]
        else:
            filteredsorted_results = sorted_results
       
            
        print(search_query.lower())
        print(searchresults)
        print(count)
                
        # lengthlist= len(searchresults)
        # print(searchresults)
        # print(lengthlist)


    return render_template("search.html",  filteredsorted_results = filteredsorted_results)
@app.route("/export_csv" ,methods=['GET'])
def export_csv():
# Convert the list of dictionaries to a Pandas DataFrame
    df = pd.DataFrame(filteredsorted_results)
    print(df.info)

# Export the DataFrame to a CSV file
    df.to_csv('output.csv', index=False, encoding='utf-8-sig')  
    filename = 'output.csv'
    return send_file(filename , as_attachment= True)

@app.route("/search/<product>", methods=[ "GET"] )
def viewresult(product):
    productdisplay =[]
    data = pd.read_csv('NLP_Dataset_Cut (1).csv')  
    for index in data.index:
        product_name = data['Product'][index]
        if product in product_name.replace("/", " or "):
            productdisplay.append(data.iloc[index])
    print(product)
    print(productdisplay)

    return render_template("searchdiscription.html", product=product, productdisplay=productdisplay )


@app.route("/filter", methods=["POST", "GET"])

def filter():
    global results
    results = []
    select = request.form.get('category')
    data = []
    count = 0

    with open("NLP_Dataset_Cut.csv", encoding="utf8") as file:
        reader = csv.reader(file)
        for row in reader: 
            newRow = row[:7]
            edits = newRow[1].replace("/"," or ")
            newRow[1] = edits 
            data.append(newRow)
        # print(data)


        for i in range(len(data)):
            if select == data[i][2]:
                if count == 50:
                    print("break triggered")
                    break
                else:
                    results.append(data[i])
                    count +=1
        
    return render_template("filter.html", select=select, results=results, count=count)

@app.route("/export_filter", methods=["POST", "GET"])
def export_filter():

    df = pd.DataFrame(results)
    df.columns = ['ASIN','Product', 'Category', 'Price', 'URL', 'Stars', 'Summary']
    # Export the DataFrame to a CSV file
    df.to_csv('output.csv', index=False)  
    filename = 'output.csv'
    return send_file(filename , as_attachment= True)

@app.route("/filter/<product>", methods=["GET"])
def filter_next(product):
    name = ""
    reviews = ""
    sentiment = ""
    confidence = ""
    nlp_review = ""
    with open("NLP_Dataset_Cut.csv", encoding="utf8") as file:
        reader = csv.reader(file)
        for row in reader: 
            newRow = row[7:11]

            if row[1].replace("/", " or ") == product:
                name = row[1]
                reviews = newRow[0]
                sentiment = newRow[1]
                confidence = newRow[2]
                nlp_review = newRow[3]
               
        
    return render_template('description.html', product=product, reviews=reviews, sentiment=sentiment, confidence=confidence, nlp_review = nlp_review, name=name)


if __name__ == '__main__':
    app.run(debug=True, port = 8000)