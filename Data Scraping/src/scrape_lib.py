from bs4 import BeautifulSoup
import requests
import time
import json
from selenium import webdriver


def getHTMLText(driver):
    scroll_pause_time = 1
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_scroll_height = driver.execute_script(
            "return document.body.scrollHeight")
        if new_scroll_height == scroll_height:
            break
        scroll_height = new_scroll_height

    html_txt = driver.page_source
    driver.quit()
    return html_txt


def getListOfTupleData(html_txt, home_link):
    soup = BeautifulSoup(html_txt, 'lxml')
    all_products_info_tag = [tag for tag in soup.find_all(
        'div', class_='product-item')]
    products_info = []

    for product_info1 in all_products_info_tag:

        product_info = ()
        # Product_Name
        name = product_info1.find('a', class_='titledekstop').text
        product_info += (name,)

        # Product_Price
        price_element = product_info1.find(
            'div', class_='product-item__price price1')
        price = price_element.text if price_element else "N/A"
        if price == 'N/A':
            price = product_info1.find(
                'span', class_='sale sale-collection').text
        price = price.split('IDR')[-1].replace('.', '').replace(' ', '')
        product_info += (price,)

        # Image Link
        image_link = product_info1.find('img', class_="image__img")['src']
        product_info += (image_link, )

        # Access product details
        details_link = home_link + product_info1.find('a')['href']
        driver2 = webdriver.Chrome()
        driver2.get(details_link)
        details_html_txt = getHTMLText(driver2)
        soup1 = BeautifulSoup(details_html_txt, 'lxml')

        # Color
        color = soup1.find('span', id='divcolorpickervalue').text
        product_info += (color,)

        # Product_ID
        product_id = soup1.find(
            'div', class_="product__sku fs-body-25 t-opacity-60").text
        product_id = product_id.split("|")[0]
        product_id = product_id.replace(' ', '')
        product_info += (product_id,)

        # Product_Details
        details_container = soup1.find(
            'div', id="accordion-content-description")
        details_tuple = details_container.find_all('li')
        details = ''
        for detail in details_tuple:
            temp = detail.text
            if details != '':
                details += ", "
            details += temp

        product_info += (details, )
        products_info.append(products_info)
        print("Getting", name)
    return products_info


def jsonStoring(products_info):
    products = {
        "products": [
            {
                'Product_Code': product[4],
                'Product_Name': product[0],
                'Image_Link': product[2],
                'Color': product[3],
                'Price': product[1],
                'Details':  product[5]
            }
            for product in products_info
        ]
    }
    products_json = json.dumps(products)
    with open('products.json', 'w') as file:
        file.write(products_json)

    # products_names = [name for name in all_products_info.find_a]
    # print(len(all_products_info))
    # product_price = [tag.href for tag in soup.find_all()]

    # print(product_name)
