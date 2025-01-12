from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import time
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(filename="books_scraper.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def scrape_books():
    books_list = []
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    page_number = 1  # Start from page 1
    while True:
        url = base_url.format(page_number)
        logging.info(f"Scraping page {page_number}...")
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad HTTP status codes
            
            soup = BeautifulSoup(response.text, 'html.parser')
            books = soup.find_all('h3')  # Book titles are inside <h3> tags
            
            if not books:
                logging.info("No books found on this page. Exiting...")
                break

            for book in books:
                title = book.find('a')['title']
                books_list.append(title)

            next_page = soup.find('li', class_='next')
            if next_page:
                page_number += 1
                time.sleep(2)  # Add a delay to avoid overloading the server
            else:
                logging.info("No more pages found.")
                break

        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred: {e}")
            break
    
    return books_list

@app.route('/')
def index():
    books = scrape_books()  # Run the scraper and get the list of books
    return render_template('index.html', books=books)  # Send books data to the front end

if __name__ == "__main__":
    app.run(debug=True)