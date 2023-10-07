import pandas as pd
data = pd.read_pickle('NLP_Dataset.pkl')
results = []
count = 0
search_query = 'asus'
for index in data.index:
    product_name = data['Product'][index]
    if search_query.lower() in product_name.lower():
        results.append(data.iloc[index])
        count +=1
    if count == 50:
        break

print(len(results))