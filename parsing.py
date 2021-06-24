import requests
import bs4 as bs
import pandas as pd

class Writer:
    def __init__(self, sale):
        self.salesDF = pd.DataFrame(
            {'category': sale.categories,
            'title': sale.titles,
            'link': sale.links
            }
        )

    def write_to_csv(self):
        csvFileContents = self.salesDF.to_csv(index=False)
        with open("kinavo.csv", "a", encoding='utf-8') as f:
            f.write(csvFileContents)

class Sales:
    def __init__(self, products):
        self.products = products
        self.categories = []
        self.titles = []
        self.links = []
        

        for product in products:
            self.categories.append(product.category)
            self.titles.append(product.title)
            self.links.append(product.link)
            

class Product:
    def __init__(self, category, title, link):
        self.category = category
        self.title = title
        self.link = link
        


def get_html(url):
    r = requests.get(url)
    return r.text


def get_data(html, url):
    soup = bs.BeautifulSoup(html, 'html.parser')
    category = soup.find('ul', class_='breadcrumb2').find_all('li')[1].a.text
    ads = soup.find('div', class_='list-view').find_all('div', class_='item')
    products = []
    for ad in ads:
        common_list = []
        title = ad.find('div', class_='listbox_title')
        link = ad.find('div', class_='listbox_title').a.get('href')
        common_list.append(category)
        common_list.append(title.text.replace('\n', ''))
        common_list.append('https://www.kivano.kg' + link)
        products.append(Product(common_list[0], common_list[1], common_list[2]))
    return products

def get_total_pages(html):
    soup = bs.BeautifulSoup(html, 'html.parser')
    pages = soup.find('ul', class_='pagination').find_all('a')[2].get('href')
    total_pages = pages.split('=')[1]
    return int(total_pages)

def get_urls(base_urls, urls):
    total_page = get_total_pages(get_html(urls))
    page_part = 'page='
    for i in range(1, total_page + 1):
        all_urls = base_urls + page_part + str(i)
        sales_1 = Sales(get_data(get_html(all_urls), base_urls))
        writer_1 = Writer(sales_1)
        writer_1.write_to_csv()

def main():
    base_url_1 = 'https://www.kivano.kg/kompyutery?'
    url_1 = 'https://www.kivano.kg/kompyutery?page=1'
    get_urls(base_url_1, url_1)
    base_url_2 = 'https://www.kivano.kg/avtotovary?'
    url_2 = 'https://www.kivano.kg/avtotovary?page=1'
    get_urls(base_url_2, url_2)
    base_url_3 = 'https://www.kivano.kg/elektronika?'
    url_3 = 'https://www.kivano.kg/elektronika?page=1'
    get_urls(base_url_3, url_3)
    base_url_4 = 'https://www.kivano.kg/odezhda-i-aksessuary?'
    url_4 = 'https://www.kivano.kg/odezhda-i-aksessuary?page=1'
    get_urls(base_url_4, url_4)


if __name__ == '__main__':
    main()