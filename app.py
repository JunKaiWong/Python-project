from flask import Flask, render_template, request, send_file
from flask_bootstrap import Bootstrap
import pandas as pd
import csv

app = Flask(__name__)
bootstrap = Bootstrap(app)

filteredsorted_results = []

@app.route("/")
def home():
        return render_template("DataVisualisation.html")


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
    df.to_csv('search_output.csv', index=False, encoding='utf-8-sig')  
    filename = 'search_output.csv'
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
    # var results is a global variable
    global results

    #creating new variables for storing csv data
    results = []
    data = []
    count = 0

    # get category name from drop down list in html
    select = request.form.get('category')
   
    # open CSV file
    with open("NLP_Dataset_Cut.csv", encoding="utf8") as file:
        #read csv file
        reader = csv.reader(file)

        #looping the csv file data
        for row in reader:
            # get all information from column 1 to 6 and insert column 8 for filter display
            newRow = row[:6] 
            newRow.insert(6, row[8])
            
            # convert all product names that have / to 'or' to allow url access
            edits = newRow[1].replace("/"," or ")
            newRow[1] = edits 
            
            # append newRow to data
            data.append(newRow)
        # print(data)

        #loop the range of data length 
        for i in range(len(data)):
            # check if category user chose match with the Category in the data column
            if select == data[i][2]:
                # display only 50 data
                if count == 50:
                    break
                else:
                    # if count has not reached 50  continue appending data to results list for display
                    results.append(data[i])
                    count +=1

    # run the filter.html template and pass variables to the html    
    return render_template("filter.html", select=select, results=results, count=count)

@app.route("/export_filter", methods=["POST", "GET"])
def export_filter():

    #Convert results list to dataframe
    df = pd.DataFrame(results)

    # add new header in dataframe
    df.columns = ['ASIN','Product', 'Category', 'Price', 'URL', 'Stars', 'Summary']

    # Export the DataFrame to a CSV file
    df.to_csv('filter_output.csv', index=False, encoding='utf-8-sig')  
    filename = 'filter_output.csv'
    return send_file(filename , as_attachment= True)

@app.route("/filter/<product>", methods=["GET"])
def filter_next(product):
    # initialize variables to pass to html
    name = ""
    reviews = ""
    sentiment = ""
    confidence = ""
    nlp_review = ""

    #open csv file
    with open("NLP_Dataset_Cut.csv", encoding="utf8") as file:
        # read csv file
        reader = csv.reader(file)

        # loop csv file to retieve column 7,8,9,10
        for row in reader: 
            

            # check if product name matches 
            if row[1].replace("/", " or ") == product:
                name = row[1]
                reviews = row[6]
                sentiment = row[9]
                confidence = round(float(row[10]),2)
                nlp_review = row[7]
               
    # return the description.html template to display to user 
    return render_template('description.html', product=product, reviews=reviews, sentiment=sentiment, confidence=confidence, nlp_review = nlp_review, name=name)


if __name__ == '__main__':
    app.run(debug=True, port = 8000)