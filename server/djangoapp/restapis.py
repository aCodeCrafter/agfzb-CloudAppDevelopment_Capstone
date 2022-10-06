import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(f'GET from {url}')
    try:
        resp = requests.get(
            url=url, params=kwargs,
            headers={'Content-Type':'application/json'})
    except:
        print('Network exception occured')
    print(f'With status {resp.status_code}')
    json_data = json.loads(resp.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(f'POST to {url}')
    try:
        resp = requests.post(url=url, json=json_payload, params=kwargs, headers={'Content-Type':'application/json'})
    except:
        print('Network exception occured')
    print(f'With status {resp.status_code}')
    json_data = json.loads(resp.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url,**kwargs):
    dealer_json_resp = get_request(url=url,params=kwargs)
    results = []
    if dealer_json_resp:
        for row in dealer_json_resp:
            results.append(
                CarDealer(
                    address=row['address'],
                    city=row['city'],
                    full_name=row['full_name'],
                    id=row['id'],
                    lat=row['lat'],
                    long=row['long'],
                    short_name=row['short_name'],
                    st=row['st'],
                    state=row['state'],
                    zip=row['zip']
                )
            )
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_sentiment_for_review(review_text):
    url = ''
    apikey = ''
    return 'None'
def get_dealer_reviews_from_cf(url,**kwargs):
    reviews_json_resp = get_request(url=url,params=kwargs)
    results = []
    if reviews_json_resp:
        for row in reviews_json_resp:
            sentiment = get_sentiment_for_review(row['review'])
            if row['purchase'] == True:
                results.append(
                    DealerReview(
                        dealership=row['dealership'],
                        name=row['name'],
                        purchase=row['purchase'],
                        review=row['review'],
                        purchase_date=row['purchase_date'],
                        car_make=row['car_make'],
                        car_model=row['car_model'],
                        car_year=row['car_year'],
                        sentiment=sentiment,
                        id=row['id'],
                    )
                )
            else:
                results.append(
                    DealerReview(
                        dealership=row['dealership'],
                        name=row['name'],
                        purchase=row['purchase'],
                        review=row['review'],
                        purchase_date=None,
                        car_make=None,
                        car_model=None,
                        car_year=None,
                        sentiment=sentiment,
                        id=row['id'],
                    )
                )
    return results
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def submit_review_to_cf(url, json_body, **kwargs):
    json_resp = post_request(url=url, json_body=json_body, params=kwargs)
    if json_resp.status_code == 200:
        return True
    else:
        print(f'An error occured while submitting a review\n Error code: {json_resp.status_code}\n Error message: {json_resp.body.message}')
        return False
