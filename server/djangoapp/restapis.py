import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview

#Import Watson packages for sentiment analyze
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

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
            print(dealer_json_resp)
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

def analyze_review_sentiments(text):
    try:
        apikey = 'QksJXRd60inex83sE5UfCH9RO20ZxRob9YPDIi6QL6he'
        url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/9ddf93cc-63ec-4953-b996-961a2e4e9c99/v1/analyze?version=2022-04-07'
        authenticator = IAMAuthenticator(apikey)

        natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2022-04-07',
            authenticator=authenticator
            )

        natural_language_understanding.set_service_url(url)
        resp = natural_language_understanding.analyze(
            text=text,
            features = Features(sentiment=SentimentOptions(targets=['dealership']))
            ).get_result()

    ##    score = resp['sentiment']['targets'][0]['score']
        label = resp['sentiment']['targets'][0]['label']
        if label in ('positive', 'negative', 'neutral'):
            return label
        else:
            print(f'Network Error IBM Watson Returned unexpected value {str(label)}')
            return ''
    except:
        print(f'Error trying to analyze {text}')
def get_dealer_reviews_from_cf(url,**kwargs):
    reviews_json_resp = get_request(url=url,params=kwargs)
    results = []
    print(reviews_json_resp)
    if reviews_json_resp:
        for row in reviews_json_resp:
            sentiment = '' #row['sentiment']
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
