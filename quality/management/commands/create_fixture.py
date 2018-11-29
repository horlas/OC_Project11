import requests
import re
import sys
import json
from collections import OrderedDict

from pathlib import Path # if you haven't already done so
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
# Additionally remove the current file's directory from sys.path
try:
    sys.path.remove(str(parent))
except ValueError: # Already removed
    pass




#########Functions to create fixtures########

def request_off(cat):
    ''' function which calls Openfoodfacts and return only the list of the products dictionnary.
    We only get the first sixty products.'''

    url_begin = "https://fr.openfoodfacts.org/cgi/search.pl?"
    payload = {
        'action': 'process',
        'tagtype_0': 'categories',
        'tag_contains_0' : 'contains',
        'tag_0' : cat,
        'tagtype_1' : 'nutrition_grades',
        'tag_contains_1' : 'contains',
        'sort_by' : 'unique_scans_n',
        'page_size' : '60',
        'axis_x' : 'energy',
        'axis_y' : 'product_n',

        'json' : '1',
     }
    response = requests.get(url_begin , params=payload)
    result = response.json()
    return result['products']

def data_process(products):
    '''function which keeps only data we need from the OpenFood Facts return'''


    # removal of products without category
    result = []
    for i, e in enumerate(products):
        try:
            test1 = e['categories']
        except KeyError:
            result.append(products[i])

        # removal of products without name
        try:
            test2 = e['product_name']
        except KeyError:
            result.append(products[i])

        # removal of products without image
        try:
            test3 = e['image_front_url']
        except KeyError:
            result.append(products[i])

    products = [x for x in products if x not in result]

    # processing of product names
    # in some case product_names have () or, inside
    # which prevents the correct operation of the rest of the program
    for i, e in enumerate(products):
        # len(list) in case length list < 6
        m1 = re.search('(\,.*?$)', e['product_name'])
        if m1 is not None:

            e['product_name'] = e['product_name'].replace(m1.group(0), '')

        m2 = re.search('(\(.*?$)', e['product_name'])
        if m2 is not None:
            e['product_name'] = e['product_name'].replace(m2.group(0), '')


    list = []

    for i in range(len(products)):

        dict = {
            "name": products[i].get('product_name', 'Non renseigné'),
            "n_grade": products[i].get('nutrition_grades', 'NC').upper(),
            "img": products[i].get('image_front_url', 'image_ingredients_small_url'),

            # keep the last category the most significant
            "category": products[i]['categories'].split(',')[-1],
            "url": products[i]['url'],
            "img_nutrition": products[i].get('image_nutrition_url', 'Non renseigné'),
            "store": products[i].get('stores', 'Non renseigné')
        }
        list.append(dict)


    # processing of product names
    # in some case product_names have () or, inside
    # which prevents the correct operation of the rest of the program
    for i in range(len(list)):     # len(list) in case lenght list < 6
        m1 = re.search('(\,.*?$)', list[i]['name'])
        if m1 is not None:
            list[i]['name'] = list[i]['name'].replace(m1.group(0), '')

        m2 = re.search('(\(.*?$)', list[i]['name'])
        if m2 is not None:
            list[i]['name'] = list[i]['name'].replace(m2.group(0), '')

    return list


def fill_database(category):
    '''function which write a file with processed data'''
    list = []
    # import category and products
    products = request_off(category)
    products = data_process(products)
    # build the data in json format

    for i, e in enumerate(products):
        dict = OrderedDict([("model", "quality.product"), ("fields", e)])
        list.append(dict)
    print("Import de la catégorie {}, {} produits".format(category, len(products)))
    list = json.dumps(list, indent=4, separators=(',', ': '), ensure_ascii=False)
    with open("quality/fixtures/dugras_data.json", "w") as file:
        file.write(list)
    return len(products)


# if __name__ == '__main__':
#     fill_database('Plats préparés')