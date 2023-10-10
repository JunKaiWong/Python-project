from flask import Flask, render_template, url_for, request, Response, send_file, redirect
from flask_bootstrap import Bootstrap
import pandas as pd
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
        data = pd.read_csv('NLP_Dataset_Cut.csv')     

        for index in data.index:
            product_name = data['Product'][index].replace("/", " ")
            if search_query.lower() in product_name.lower():
                searchresults.append(data.iloc[index])
                count +=1

        sorted_results = sorted(searchresults, key = lambda x: x['Stars'], reverse=True)

        if len(sorted_results) >= 50:
            filteredsorted_results = sorted_results[:51]
        else:
            filteredsorted_results = sorted_results
       
            
        print(search_query.lower())
        print(searchresults)
        print(count)

    return render_template("search.html", filteredsorted_results = filteredsorted_results)

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
    data = pd.read_csv('NLP_Dataset_Cut.csv')  
    for index in data.index:
        product_name = data['Product'][index]
        if product in product_name.replace("/", " or "):
            productdisplay.append(data.iloc[index])
    print(product)
    print(productdisplay)

    return render_template("searchdiscription.html", product=product, productdisplay=productdisplay )


@app.route("/filter", methods=["POST", "GET"])
def filter():
     select = request.form.get('category')
     results = []
     data = []
     count = 0
     with open("NLP_Dataset_Edited.csv", encoding="utf8") as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader: 
            newRow = row[:7]
            data.append(newRow)
        


        for i in range(len(data)):
            if select == data[i][1]:
                if count == 50:
                    print("break triggered")
                    break
                else:
                    results.append(data[i])
                    count +=1
                    # print("This is results",results)
        
     return render_template("filter.html", select=select, header=header, results=results, count=count)


if __name__ == '__main__':
    app.run(debug=True, port = 8000)