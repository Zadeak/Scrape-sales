import requests
from bs4 import BeautifulSoup
import re
import json


def connect(url):
    try:
        result = requests.get(url)
    except Exception:
        print("Failed to connect")
        print("Contact that brain dead developer to fix this monstrosity of a program")
        input("Press any key to finish")
        return None
    src = result.content
    soup = BeautifulSoup(src, "html.parser")
    return soup
def get_next_page_url(soup):

    try:
        next_page_link = soup.select("a.pagination__link.pagination__link--next")[0].get('href')
    except Exception:
        print("Done")
        last_page = True
        next_page_link = None
        return next_page_link, last_page
    last_page = False
    return next_page_link, last_page

def spider(link):
    last_page = False

    file = open("data.json", 'w')

    data_list = []
    while last_page == False:
        print("Connecting", link)
        soup = connect(link)
        Needed_divs = allProductsDivs(soup)

        for div in Needed_divs:
            compiled_data = compile_data(div)
            data_list.append(compiled_data)

        link, last_page = get_next_page_url(soup)
        #print("link",link,type(link),'last_page',last_page)
        print("Next page")

    output_data(data_list, file)
    file.close()
    return True

def compile_data(div):
    compiled_data = {}
    compiled_data['title'] = get_title(div)
    compiled_data['old_cost']  = clean_price(old_price(div))
    compiled_data['new_price']  = clean_price(new_price(div))
    compiled_data['link']  = get_link(div)
    compiled_data['picture']  = get_img(div)


    return compiled_data


def output_data(dict,file):
    json.dump(dict,file)


def allProductsDivs(soup):
    links = soup.find_all('a', class_='products-grid__link product-image')
    Needed_divs = []
    for line in links:
        if line.find(class_="old-price") is not None:
            Needed_divs.append(line)
        else:
            continue

    return Needed_divs


def get_link(tag):
    return tag.get('href')
def get_title(tag):
    return tag.get('title')

def get_img(tag):

    Img_list = []
    img_div = tag.select('img')
    for img in img_div:
        Img_list.append(img)

    if len(Img_list) > 1 :
        img = Img_list[1].get('src')
    else:
        img = Img_list[0].get('src')
    return img




print("...................................")
print(".............Starting..............")

"""функция, найти старую цену"""
def old_price(tag):
    price = tag.find_all(id=re.compile('^old-price-'))[0].get_text()
    return price


"""функция, найти новую цену"""
def new_price(tag):
    price = tag.find_all(id=re.compile('^product-price-'))[0].get_text()
    return price


def clean_price(text):
    digits = [ symbol for symbol in text if symbol.isdigit() or symbol == ","]
    cleaned_text = ''.join(digits)
    if not cleaned_text:
        return None
    else:
        return cleaned_text






