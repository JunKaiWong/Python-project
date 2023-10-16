from flask import Flask, render_template, request, send_file
from flask_bootstrap import Bootstrap
import pandas as pd
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import seaborn as sns
import ast
from io import BytesIO
import base64
app = Flask(__name__)
bootstrap = Bootstrap(app)

#Function to convert string to list
def str_to_list(review_str):
    return ast.literal_eval(review_str)

#modify sentiment based on confidence level
def modify_sentiment(row):
    sentiment = row['Sentiment']
    confidence = row['Confidence']
    if confidence < 0.75:
        return 'Neutral'
    elif confidence >= 0.75 and sentiment==str('Positive'):
        return 'Positive'
    else:
        return 'Negative'


@app.route("/" ,methods=["POST", "GET"])
def home():
    graphlist = []

    if request.method == 'POST':

        displaygraph = request.form.get('graphs')   

        if displaygraph == "piechart":
            plt.clf()

            df = pd.read_csv('NLP_Dataset_Cut.csv')  
            #use for piechart and scattergraph
            df2=df[['Category', 'Product']]
            category_counts=df2.groupby('Category')['Product'].count().reset_index()
            labels=category_counts['Category']
            category_counts_data=category_counts['Product']

            total_products = category_counts_data.sum()
            #create a pie chart
            plt.pie(category_counts_data, labels=labels, autopct='%.1f%%',startangle=140)
            plt.title('Product Distribution by Category')
            plt.text(1.0, 0.0, f'Total Products: {total_products}', horizontalalignment='center', verticalalignment='center', fontsize=11, transform=plt.gca().transAxes)

            # Save the graph as a PNG image
            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)

            # Embed the image data in the HTML
            plot_url = base64.b64encode(img.read()).decode('utf-8')
            graphlist.append(plot_url)

        elif displaygraph == "histograph":
            plt.clf()

            df = pd.read_csv('NLP_Dataset_Cut.csv')  

            plt.figure(figsize=(8, 6))
            #create a histogram plot of the 'Stars' column in the df
            plt.hist(df['Stars'], bins=5, color='skyblue', edgecolor='black', alpha=0.7)
            plt.title('Star Rating Distribution')
            plt.xlabel('Stars')
            plt.ylabel('Count')
            plt.ylim(0,3000)

            # Save the graph as a PNG image
            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)

            # Embed the image data in the HTML
            plot_url = base64.b64encode(img.read()).decode('utf-8')
            graphlist.append(plot_url)

        elif displaygraph == "bargraph":
            plt.clf()

            df = pd.read_csv('NLP_Dataset_Cut.csv')  
            df3 = df[['Category', 'Stars']]
            # Group the data by 'Category' and calculate the mean of 'Stars' for each category
            df3.groupby('Category').mean()
            
            # Calculate the mean 'Stars' for each category and reset the index
            category_means = df3.groupby('Category')['Stars'].mean().reset_index()
            
            # Sort the categories based on the mean 'Stars' in descending order
            category_means = category_means.sort_values(by='Stars', ascending=False)
            # Set 'Category' as the index for the DataFrame
            category_means.set_index('Category', inplace=True)
            
            # Create a bar plot with the category as the x-axis and the average rating as the y-axis
            ax = category_means.plot(kind='bar', legend=False)

            # Add grid lines
            ax.yaxis.grid(True, linestyle='--', alpha=0.7, zorder=0)

            plt.xlabel('Category')
            plt.ylabel('Average Rating')
            plt.title('Average Rating by Category')

            plt.xticks(rotation=0, fontsize=6)
            plt.ylim(0, 5)

            # Save the graph as a PNG image
            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)

            # Embed the image data in the HTML
            plot_url = base64.b64encode(img.read()).decode('utf-8')
            graphlist.append(plot_url)

        elif displaygraph == "scattergraph":
            plt.clf()
            df = pd.read_csv('NLP_Dataset_Cut.csv') 
            
            # Convert the 'Reviews' column to a list of lists
            df['Reviews'] = df['Reviews'].apply(str_to_list)

            # Calculate the sum of reviews per product and create a new column for it
            df['Reviews Sum Per Product'] = df['Reviews'].apply(lambda x: len(x))
            
            # Select the required columns for further analysis
            df[['Category', 'Product', 'Reviews Sum Per Product']]
            df2=df[['Category', 'Product']]
            
            # Group the data by 'Category' and count the number of products in each category
            category_counts=df2.groupby('Category')['Product'].count().reset_index()
            # Calculate the sum of reviews per product for each category
            category_sum = df.groupby('Category')['Reviews Sum Per Product'].sum().reset_index()

            # Merge the two DataFrames based on the 'Category' column
            result_df = pd.merge(category_counts, category_sum, on='Category')

            result_df.rename(columns={'Product': 'Product Count', 'Reviews Sum Per Product': 'Reviews Sum'}, inplace=True)

            plt.figure(figsize=(10, 6))

           # Scatter plot
            scatter = plt.scatter(result_df['Product Count'], result_df['Reviews Sum'], c=result_df['Category'].astype('category').cat.codes, cmap='viridis', s=100)
            plt.xlabel('Product Count')
            plt.ylabel('Reviews Count')
            plt.title('Reviews Count vs. Product Count by Category')

            # Create a custom colorbar with product category names
            colorbar = plt.colorbar(scatter, label='Category')
            category_names = result_df['Category'].unique()
            colorbar.set_ticks(range(len(category_names)))
            colorbar.set_ticklabels(category_names)


            # Save the graph as a PNG image
            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)

            # Embed the image data in the HTML
            plot_url = base64.b64encode(img.read()).decode('utf-8')
            graphlist.append(plot_url)
    
        elif displaygraph == "intervalplot":
            plt.clf()
            df = pd.read_csv('NLP_Dataset_Cut.csv') 

            plt.figure(figsize=(8, 6))
            # Create a histogram plot of the 'Confidence' column with kernel density estimation (KDE)
            sns.histplot(df['Confidence'], kde=True, color='skyblue')
            sns.kdeplot(df['Confidence'], color='red', linestyle='--', label='Kernel Density Estimate')
            
            # Calculate the confidence interval using the np.percentile function
            confidence_interval = np.percentile(df['Confidence'], [2.5, 97.5])
            lower_bound, upper_bound = confidence_interval

            # Add confidence interval lines to the plot
            plt.axvline(lower_bound, color='green', linestyle=':', label='95% Confidence Interval')
            plt.axvline(upper_bound, color='green', linestyle=':')

            plt.xlabel('Confidence Values')
            plt.ylabel('Number of Sentiments')
            plt.title('Confidence Interval Plot')

            plt.legend()

            # Save the graph as a PNG image
            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)

            # Embed the image data in the HTML
            plot_url = base64.b64encode(img.read()).decode('utf-8')
            graphlist.append(plot_url)

        elif displaygraph == "subplot":
            plt.clf()
            df = pd.read_csv('NLP_Dataset_Cut.csv') 
              #use for subplot
            df5=df[['Sentiment', 'Confidence']]
            # Group the data by 'Sentiment' and calculate the mean for each group
            df5.groupby('Sentiment').mean()

            plt.figure(figsize=(10, 6))
            # Create a subplot with 1 row, 2 columns, and select the first subplot
            plt.subplot(1, 2, 1)
            sns.boxplot(x='Sentiment', y='Confidence', data=df5[df5['Sentiment'] == 'Positive'])
            plt.title('Positive Sentiment Confidence Levels')
            plt.xlabel('Sentiment')
            plt.ylabel('Confidence')
            
            # Create a subplot with 1 row, 2 columns, and select the second subplot
            plt.subplot(1, 2, 2)
            sns.boxplot(x='Sentiment', y='Confidence', data=df5[df5['Sentiment'] == 'Negative'])
            plt.title('Negative Sentiment Confidence Levels')
            plt.xlabel('Sentiment')
            plt.ylabel('Confidence')

            plt.tight_layout()

            # Save the graph as a PNG image
            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)

            # Embed the image data in the HTML
            plot_url = base64.b64encode(img.read()).decode('utf-8')
            graphlist.append(plot_url)

        elif displaygraph == "sentimentgraph":
            plt.clf()
            df = pd.read_csv('NLP_Dataset_Cut.csv') 
            # Create a new 'Modified Sentiment' column without overwriting 'Sentiment'
            df['Modified Sentiment'] = df.apply(modify_sentiment, axis=1)

            # Create a DataFrame 'modified_df' containing 'Modified Sentiment' and 'Confidence'
            modified_df = df[['Modified Sentiment', 'Confidence']]
            # Calculate the counts of each sentiment in the original 'Sentiment' column
            sentiment_counts = df['Sentiment'].value_counts()
            # Filter the 'modified_df' for entries where 'Modified Sentiment' is 'Positive'
            positive_sentiment_df = modified_df[modified_df['Modified Sentiment'] == 'Positive']
            
            # Calculate the counts of each modified sentiment in the 'Modified Sentiment' column
            sentiment_counts = modified_df['Modified Sentiment'].value_counts()

            plt.figure(figsize=(8, 6))
            # Plot the counts of each sentiment as a bar plot
            sentiment_counts.plot(kind='bar', color='skyblue')
            plt.title('Sentiment Distribution')
            plt.xlabel('Sentiment')
            plt.ylabel('Count')
            plt.ylim(0,3500)

            # Save the graph as a PNG image
            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)

            # Embed the image data in the HTML
            plot_url = base64.b64encode(img.read()).decode('utf-8')
            graphlist.append(plot_url)

    return render_template("DataVisualisation.html", graphlist = graphlist ) 


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
        print(filteredsorted_results)
    #return the variables needed HTML
    return render_template("search.html",  filteredsorted_results = filteredsorted_results)

@app.route("/export_csv" ,methods=['GET'])
def export_csv():
# Convert the list of dictionaries to a Pandas DataFrame
    df = pd.DataFrame(filteredsorted_results)

# Export the DataFrame to a CSV file
    df.to_csv('csvoutput/search_output.csv', index=False, encoding='utf-8-sig')  
    filename = 'csvoutput/search_output.csv'
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
    # var results is a global variable to be used for exporting
    global filterFullResults

    #creating new variables for storing csv data
    results = []
    data = []
    filterFullResults  = []
    newRowAll = []
    count = 0
    counter2 = 0

    # get category name from drop down list in html
    select = request.form.get('category')
   
    # open CSV file
    with open("NLP_Dataset_Cut.csv", encoding="utf8") as file:
        #read csv file
        reader = csv.reader(file)

        #looping the csv file data
        for row in reader:
            # get all information from column 1 to 6 and insert column 8 for filter display
            newRow = row[1:6] 
            newRow.insert(6, row[8])

            newRowAll.append(row)
           
            # convert all product names that have / to 'or' to allow url access
            edits = newRow[0].replace("/"," or ")
            newRow[0] = edits 
            
            # append newRow to data
            data.append(newRow)

            #sort data based on rating(highest to lowest)
            data =  sorted(data, key = lambda x: x[4], reverse=True)

        #loop the range of data length 
        for i in range(len(data)):
            # check if category user chose match with the Category in the data column

            if select == data[i][1]:
                # display only 50 data
                if count >= 50:
                    break
                else:
                    count +=1
                    # if count has not reached 50  continue appending data to results list for display
                    results.append(data[i])

        # looping range of newRowAll Length
        for index in range(len(newRowAll)):
            # display only 50 data for all data columns
            if select == newRowAll[index][2]:
                
                if counter2 >= 50:
                    break
                else:
                    #append all the data to filterFullResults to be exported into csv
                    counter2 +=1
                    filterFullResults.append(newRowAll[index])
                    # sort list based on rating 
                    filterFullResults = sorted(filterFullResults, key = lambda x: x[5], reverse=True )
           
                

    # run the filter.html template and pass variables to the html    
    return render_template("filter.html", select=select, results=results, count=count, filterFullResults=filterFullResults)

@app.route("/export_filter", methods=["POST", "GET"])
def export_filter():

    #Convert results list to dataframe
    df = pd.DataFrame(filterFullResults)
    # add column header
    df.columns = ['ASIN','Product', 'Category', 'Price', 'URL', 'Stars','Reviews', 'NLP_Reviews', 'Summary', 'Sentiment', 'Confidence']

    # Export the DataFrame to a CSV file
    df.to_csv('csvoutput/filter_output.csv', index=False, encoding='utf-8-sig')  
    filename = 'csvoutput/filter_output.csv'
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
