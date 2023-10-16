from flask import Flask, render_template, url_for, request, Response, send_file, redirect
from flask_bootstrap import Bootstrap
import pandas as pd
import csv

app = Flask(__name__)
bootstrap = Bootstrap(app)

searchresults = []
sorted_results = sorted(searchresults, key = lambda x: x['Stars'], reverse=True)

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
        
        count = 0
        data = pd.read_pickle('NLP_Dataset.pkl')
        print(type(data['Reviews'][0]))
        print(search_query)
        for index in data.index:
            product_name = data['Product'][index]
            if search_query.lower() in product_name.lower():
                searchresults.append(data.iloc[index])
                sorted_results = sorted(searchresults, key = lambda x: x['Stars'], reverse=True)
                count +=1
                
            if count == 50:
                break
                
        lengthlist= len(searchresults)
        print(searchresults)
        print(lengthlist)


    return render_template("search.html", sorted_results = sorted_results, lengthlist=lengthlist)

@app.route("/export_csv")
def export_csv():
# Convert the list of dictionaries to a Pandas DataFrame
    df = pd.DataFrame(searchresults)

# Export the DataFrame to a CSV file
    df.to_csv('output.csv', index=False)  
    filename = 'output.csv'
    return send_file(filename , as_attachment= True)

"""@app.route('/viewresult', methods=["POST", "GET"] )
def viewresult():
    if request.method == 'POST':
        productname = request.form.get('productname')
        viewitem=[]
        data = pd.read_pickle('NLP_Dataset.pkl')
        print(productname)
        for index in data.index:
            product_name = data['Product'][index]
            if productname in product_name:
                viewitem.append(data.iloc[index])
        print(viewitem )
        return render_template('viewresult.html',viewitem=viewitem)"""




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