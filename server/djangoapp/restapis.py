import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    #print(kwargs)
    try:
        # Call get method of requests library with URL and parameters
        if ("api_key" in kwargs):
            requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred!!")
    status_code = response.status_code
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def post_request(url, json_payload, **kwargs):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    jsonPayload = json.dumps(json_payload)
    #print(jsonPayload)
    #print(url)
    try:
        response = requests.post(url, data=jsonPayload, headers=headers)
        #response = requests.post(url, data=jsonPayload)
        #response = requests.post(url, json=jsonPayload, params=kwargs)
    except:
        print("Error in POST")
    #print("POST Response")
    #print(response.status_code)
    #print(response.headers)
    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    #print(url)
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["entries"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealers_by_state(url, st):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, st=st)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["entries"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in dealer object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"], st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

def get_dealers_by_id(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["entries"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in dealer object
            if dealer["id"] == dealerId:
                dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                    id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                    short_name=dealer["short_name"], st=dealer["st"], zip=dealer["zip"])
                results.append(dealer_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    #print(text)
    api_key = "VwLO-6XGTZ_n52z5AbBcgc4jFJxTijC36NRACGH_7UFJ"
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/1da2af05-b944-4a7f-afd0-012e1f5a6057"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version = '2020-08-01',
        authenticator = authenticator
    )
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze(
        text = text,
        language='en',
        features = Features(sentiment = SentimentOptions())
    ).get_result()
    
    return response["sentiment"]["document"]["label"]

def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        #print(json_result)
        # Get the row list in JSON as reviews
        reviews = json_result["docs"]
        # For each dealer object
        for review in reviews:
            # Create a DealerReview object with values in review object
            if "purchase_date" in review:
                dealerReview_obj = DealerReview(dealership=review["dealership"], name=review["name"], purchase=review["purchase"],
                                    review=review["review"], purchase_date=review["purchase_date"], car_make=review["car_make"],
                                    car_model=review["car_model"],car_year=review["car_year"], sentiment=analyze_review_sentiments(review["review"]))
                results.append(dealerReview_obj)
            else:
                dealerReview_obj = DealerReview(dealership=review["dealership"], name=review["name"], purchase=review["purchase"],
                                    review=review["review"], sentiment=analyze_review_sentiments(review["review"]))
                results.append(dealerReview_obj)          
    return results

