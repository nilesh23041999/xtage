import requests

# Base URL for Google Books API
GOOGLE_BOOKS_API_URL = 'https://www.googleapis.com/books/v1/'
API_KEY =  'Your_API_key'



def fetch_from_google_books_api(endpoint, params=None):
    
    
    if params is None:
        params = {}
    params['key'] = API_KEY
    url = f'{GOOGLE_BOOKS_API_URL}{endpoint}'
    response = requests.get(url, params=params)
    response.raise_for_status()  
    return response.json()






def search_books(params):
  
    return fetch_from_google_books_api('volumes', params=params)





def get_book(book_id):
    return fetch_from_google_books_api(f'volumes/{book_id}')






def trim_book_data(items, fields):
    
    trimmed_data = []
    for item in items:
        volume_info = item.get("volumeInfo", {})
        trimmed_item = {}
        for field in fields:
            trimmed_item[field] = volume_info.get(field, "Not Available")
        trimmed_data.append(trimmed_item)
    return trimmed_data
