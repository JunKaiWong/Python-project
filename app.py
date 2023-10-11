from flask import Flask, render_template, request, send_file
from flask_bootstrap import Bootstrap
import pandas as pd
import csv

app = Flask(__name__)
bootstrap = Bootstrap(app)

filteredsorted_results = []


@app.route("/")
def home():
        return render_template("index.html")


@app.route("/search", methods=["POST", "GET"] )
def search():
    #make the search list as global variable 
    global filteredsorted_results

    #check if there is any POST request on the HTML 
    if request.method == 'POST':
        #get the POST request variable 
        search_query = request.form.get('dataresult')    
        #initialised the lists into empty
        searchresults = []
        sorted_results=[]
        #read dataset
        data = pd.read_csv('NLP_Dataset_Cut.csv')     
        #use for loop to get the search results through Product name
        for index in data.index:
            product_name = data['Product'][index] 
            #initialised the POST request variable and dataframe Product name into smaller case
            if search_query.lower() in product_name.lower():
                #append the search result into searchresults list
                searchresults.append(data.iloc[index])
        #sort the searchresults list by Stars rating  
        sorted_results = sorted(searchresults, key = lambda x: x['Stars'], reverse=True)
        #display on the top 50 product results in the searchresults list
        if len(sorted_results) >= 50:
            filteredsorted_results = sorted_results[:51]
        # if the product results are less than 50, display all of the products
        else:
            filteredsorted_results = sorted_results
       
    #return the variables needed HTML
    return render_template("search.html",  filteredsorted_results = filteredsorted_results)

@app.route("/export_csv" ,methods=['GET'])
def export_csv():
# Convert the list of dictionaries to a Pandas DataFrame
    df = pd.DataFrame(filteredsorted_results)

# Export the DataFrame to a CSV file
    df.to_csv('output.csv', index=False, encoding='utf-8-sig')  
    filename = 'output.csv'
    return send_file(filename , as_attachment= True)

@app.route("/search/<product>", methods=[ "GET"] )
def viewresult(product):
    #initialised the lists into empty
    productdisplay =[]
    #read dataset
    data = pd.read_csv('NLP_Dataset_Cut.csv')  
    #use for loop to get the search results through 'ASIN'
    for index in data.index:
        product_name = data['ASIN'][index]
        #check if the ASIN from the product matches with ASIN's dataset
        if product in product_name:
            #append the result into productdisplay list
            productdisplay.append(data.iloc[index])

    #return the variables needed HTML
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
            newRow = row[:6] 
            newRow.insert(6, row[8])
            
            # edits = newRow[1].replace("/"," or ")
            # newRow[1] = edits 
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
        
    return render_template("filter.html", select=select, results=results, count=count, selection=select)

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