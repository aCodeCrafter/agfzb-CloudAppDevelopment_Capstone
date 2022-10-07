import json
import requests
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def analyze_review_sentiments(text):
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
