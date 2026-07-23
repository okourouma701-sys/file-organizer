import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

def scrape_books():
    print('Scraping books...')
    all_data = []
    for page in range(1, 6):
        url = 'https://books.toscrape.com/catalogue/page-' + str(page) + '.html'
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('article', class_='product_pod')
        for book in books:
            title = book.find('h3').find('a')['title']
            price = book.find('p', class_='price_color').text.replace('£', '')
            all_data.append({'Title': title, 'Price': float(price)})
    df = pd.DataFrame(all_data)
    df.to_csv('books_report.csv', index=False)
    print('Scraped', len(df), 'books and saved to CSV!')
    return df

def show_stats(df):
    print('\n--- STATISTICS ---')
    print('Average price: £', round(df['Price'].mean(), 2))
    print('Cheapest: £', df['Price'].min())
    print('Most expensive: £', df['Price'].max())

def make_chart(df):
    top10 = df.sort_values('Price', ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    plt.barh(top10['Title'], top10['Price'], color='skyblue')
    plt.xlabel('Price (£)')
    plt.title('Top 10 Most Expensive Books')
    plt.tight_layout()
    plt.savefig('report_chart.png')
    print('Chart saved!')

data = scrape_books()

while True:
    print('\n1 - Show statistics')
    print('2 - Create chart')
    print('3 - Quit')
    choice = input('Choose: ')
    if choice == '1':
        show_stats(data)
    elif choice == '2':
        make_chart(data)
    elif choice == '3':
        print('Goodbye!')
        break