import csv
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

# Reads csv from main.py into a dataframe
data = pd.read_csv('results.csv')
url_list = data['Url'].tolist()
asin_list = data['ASIN'].tolist()


def get_url(asin, page_number):
    # Loads review page for specific product and sort by recent
    template = ('https://amazon.sg/product-reviews/{}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews'
                '&sortBy=recent')
    # Adds ASIN value into '{}' from template
    url = template.format(asin)
    # Appends page number to end of link
    url += '&pageNumber={}'.format(page_number)
    return url


def extract_reviews(item):
    # Retrieve review title by pointing to HTML element containing it
    try:
        review_title = item.find('span', {'data-hook': 'review-title'})
        title = review_title.find('span').get_text()
    # Returns empty string if review title not found instead of crashing program
    except AttributeError:
        title = ''

    try:
        review_element = item.find('span', {'data-hook': 'review-body'})
        review = review_element.find('span').get_text()
    except AttributeError:
        review = ''

    try:
        rating = item.i.text
    except AttributeError:
        rating = ''

    result = (rating, title, review)
    return result


def main():
    driver = webdriver.Chrome()
    records = []

    # Loops through linked pairs of URL and ASIN combined
    for link, asin in zip(url_list, asin_list):
        page_number = 1
        # Restricts loop to 10 pages worth of reviews
        while page_number <= 10:
            url = get_url(asin, page_number)
            driver.get(url)
            # points BeautifulSoup to parse HTML elements
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            results = soup.findAll('div', {'class': 'a-section celwidget'})

            # If no reviews found, break out of loop
            if not results:
                break

            # Puts extracted reviews, corresponding ASIN and URL together
            for item in results:
                record = (asin,) + extract_reviews(item) + (url,)
                records.append(record)

            page_number += 1

    driver.close()

    with open('reviews.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ASIN', 'Rating', 'Title', 'Review', 'URL'])
        writer.writerows(records)


main()
