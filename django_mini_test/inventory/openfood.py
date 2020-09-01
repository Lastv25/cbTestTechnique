import requests

base_url = 'https://fr.openfoodfacts.org/api/v0/product/'

def getOpenFood(gtin):
    # Url creation for get request
    url = base_url+gtin+'.json'
    
    # Executing the request
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)

    # parsing the response for pertinent information
    productjson = r.json()['product']
    return productjson['product_name'], productjson['image_url']
