from datetime import datetime
import requests
import csv
import bs4

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
REQUEST_HEADER = {'User-Agent':
                  USER_AGENT,
                  'Accept-Language': 'en-US, en;q=0.5'}


def get_page_html(url):
    res = requests.get(url=url, headers=REQUEST_HEADER)
    return res.content

def get_product_title(soup):
    product_title = soup.find('h1', class_='product_title entry-title elementor-heading-title elementor-size-default')
    return product_title.text.strip()
  
def get_product_stock(soup):
  stock_spans = soup.find_all("p",class_="ast-stock-detail")
  for span in stock_spans:
    stock = span.text.strip().replace('Availability:',"").replace("in stock",'').replace('(can be backordered)',"")
    return stock

def get_product_price(soup):
    span=soup.find('p',class_='price')
    return span.text.strip().replace('R', '').replace(',', '').replace('Including VAT','')
  
def extract_product_info(url):
    product_info = {}
    print(f'Scraping URL: {url}')
    html = get_page_html(url)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    product_info['price'] = get_product_price(soup)
    product_info['title'] = get_product_title(soup)
    product_info['stock'] = get_product_stock(soup)
    return product_info







if __name__=='__main__':
    products_data = []
    with open('links.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            url = row[0]
            products_data.append(extract_product_info(url))
    output_file_name = 'output-{}.csv'.format(
        datetime.today().strftime("%m-%d-%Y"))
    with open(output_file_name, 'w') as outputfile:
        writer = csv.writer(outputfile)
        writer.writerow(products_data.pop().keys())
        for product in products_data:
            writer.writerow(product.values())

