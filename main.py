import csv
from bs4 import BeautifulSoup
from selenium import webdriver


def get_url(search_term):
    # Search term contained in '{}'
    template = 'https://www.amazon.sg/s?k={}&s=review-rank&ref=nb_sb_noss_1'
    # Replaces empty space with '+' to work in link
    search_term = search_term.replace(' ', '+')
    url = template.format(search_term)
    # Appends page number at end of url to cycle
    url += '&page={}'
    return url


def extract_record(item):
    # Retrieve product name by pointing to HTML element containing it
    atag = item.find('a', 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
    description = atag.text.strip()
    url = 'https://www.amazon.sg' + atag.get('href')

    # Retrieve product ASIN by pointing to HTML element containing it
    asin = item['data-asin']

    try:
        # Retrieve product price by pointing to HTML element containing it
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return

    try:
        # Retrieve product rating by pointing to HTML element containing it
        rating = item.i.text
    except AttributeError:
        # Returns empty string if rating not found instead of crashing program
        rating = ''

    result = (description, asin, price, rating, url)

    return result


def main(search_term):
    # Initialize webdriver
    driver = webdriver.Chrome()

    records = []
    url = get_url(search_term)

    # Amazon has max 20 pages for each product search
    for page in range(1, 21):
        # loops through each page
        driver.get(url.format(page))
        # points BeautifulSoup to parse HTML elements
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.findAll('div', {'data-component-type': 's-search-result'})

        for item in results:
            record = extract_record(item)
            # If able to retrieve any items, append to record list
            if record:
                records.append(record)

    driver.close()

    # Saves final records into csv file
    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'ASIN', 'Price', 'Rating', 'Url'])
        writer.writerows(records)


# Execute program with search term
main('ddr5 ram')
